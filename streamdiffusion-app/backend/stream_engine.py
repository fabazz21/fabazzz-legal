"""
StreamDiffusion Engine - Core pipeline for real-time image generation
"""
import torch
from diffusers import AutoencoderTiny, StableDiffusionPipeline
from streamdiffusion import StreamDiffusion
from streamdiffusion.image_utils import postprocess_image
import numpy as np
from PIL import Image
import threading
import queue


class StreamDiffusionEngine:
    """Real-time image generation engine using StreamDiffusion"""

    def __init__(
        self,
        model_id: str = "stabilityai/sd-turbo",
        use_tiny_vae: bool = True,
        use_lcm_lora: bool = False,
        device: str = "cuda",
        dtype=torch.float16,
    ):
        self.model_id = model_id
        self.device = device
        self.dtype = dtype
        self.use_tiny_vae = use_tiny_vae
        self.use_lcm_lora = use_lcm_lora

        self.pipe = None
        self.stream = None
        self.is_initialized = False
        self.current_prompt = ""

        print(f"Initializing StreamDiffusion with {model_id}...")
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        """Initialize the Stable Diffusion pipeline"""
        try:
            # Load base model
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=self.dtype,
            ).to(self.device)

            # Initialize StreamDiffusion wrapper
            self.stream = StreamDiffusion(
                self.pipe,
                t_index_list=[0, 16, 32, 45],  # Timestep indices for generation
                torch_dtype=self.dtype,
            )

            # Load LCM-LoRA if enabled (for faster generation)
            if self.use_lcm_lora:
                print("Loading LCM-LoRA...")
                self.stream.load_lcm_lora()
                self.stream.fuse_lora()

            # Use TinyVAE for faster decoding
            if self.use_tiny_vae:
                print("Loading TinyVAE...")
                tiny_vae = AutoencoderTiny.from_pretrained(
                    "madebyollin/taesd",
                    torch_dtype=self.dtype,
                ).to(self.device)
                self.stream.vae = tiny_vae

            self.is_initialized = True
            print("StreamDiffusion engine initialized successfully!")

        except Exception as e:
            print(f"Error initializing pipeline: {e}")
            raise

    def prepare(self, prompt: str, negative_prompt: str = "", num_inference_steps: int = 50):
        """Prepare the pipeline with a prompt"""
        try:
            self.current_prompt = prompt
            self.stream.prepare(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=1.0,  # CFG scale
            )
            print(f"Pipeline prepared with prompt: {prompt}")
        except Exception as e:
            print(f"Error preparing pipeline: {e}")
            raise

    def generate_txt2img(self, prompt: str = None) -> Image.Image:
        """Generate image from text prompt"""
        if prompt and prompt != self.current_prompt:
            self.prepare(prompt)

        try:
            # Generate image
            output_image = self.stream.txt2img()

            # Post-process and convert to PIL Image
            if isinstance(output_image, torch.Tensor):
                output_image = postprocess_image(output_image, output_type="pil")[0]

            return output_image
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def generate_img2img(self, input_image: Image.Image, prompt: str = None) -> Image.Image:
        """Generate image from input image"""
        if prompt and prompt != self.current_prompt:
            self.prepare(prompt)

        try:
            # Convert PIL Image to tensor if needed
            if isinstance(input_image, Image.Image):
                input_image = np.array(input_image)
                input_image = torch.from_numpy(input_image).permute(2, 0, 1).unsqueeze(0)
                input_image = input_image.float() / 255.0
                input_image = input_image.to(self.device, dtype=self.dtype)

            # Generate image
            output_image = self.stream(input_image)

            # Post-process and convert to PIL Image
            if isinstance(output_image, torch.Tensor):
                output_image = postprocess_image(output_image, output_type="pil")[0]

            return output_image
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def cleanup(self):
        """Cleanup resources"""
        if self.stream:
            del self.stream
        if self.pipe:
            del self.pipe
        torch.cuda.empty_cache()
        print("StreamDiffusion engine cleaned up")


class StreamGenerator:
    """Thread-safe stream generator for continuous generation"""

    def __init__(self, engine: StreamDiffusionEngine):
        self.engine = engine
        self.input_queue = queue.Queue(maxsize=1)
        self.output_queue = queue.Queue(maxsize=1)
        self.running = False
        self.thread = None

    def start(self):
        """Start the generation thread"""
        self.running = True
        self.thread = threading.Thread(target=self._generation_loop)
        self.thread.daemon = True
        self.thread.start()
        print("Stream generator started")

    def stop(self):
        """Stop the generation thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("Stream generator stopped")

    def _generation_loop(self):
        """Main generation loop running in separate thread"""
        while self.running:
            try:
                # Get input from queue (with timeout)
                try:
                    input_data = self.input_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                # Generate image based on input type
                if input_data["type"] == "text":
                    output = self.engine.generate_txt2img(input_data["prompt"])
                elif input_data["type"] == "image":
                    output = self.engine.generate_img2img(
                        input_data["image"],
                        input_data.get("prompt")
                    )
                else:
                    continue

                # Put output in queue (replace if full)
                try:
                    self.output_queue.put_nowait(output)
                except queue.Full:
                    try:
                        self.output_queue.get_nowait()
                        self.output_queue.put_nowait(output)
                    except:
                        pass

            except Exception as e:
                print(f"Error in generation loop: {e}")

    def send_prompt(self, prompt: str):
        """Send text prompt for generation"""
        try:
            self.input_queue.put_nowait({"type": "text", "prompt": prompt})
        except queue.Full:
            try:
                self.input_queue.get_nowait()
                self.input_queue.put_nowait({"type": "text", "prompt": prompt})
            except:
                pass

    def send_image(self, image: Image.Image, prompt: str = None):
        """Send image for img2img generation"""
        try:
            self.input_queue.put_nowait({
                "type": "image",
                "image": image,
                "prompt": prompt
            })
        except queue.Full:
            try:
                self.input_queue.get_nowait()
                self.input_queue.put_nowait({
                    "type": "image",
                    "image": image,
                    "prompt": prompt
                })
            except:
                pass

    def get_latest_image(self) -> Image.Image:
        """Get the latest generated image"""
        try:
            return self.output_queue.get_nowait()
        except queue.Empty:
            return None
