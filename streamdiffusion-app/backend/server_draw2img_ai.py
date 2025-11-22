"""
Flask server for real-time drawing-to-image with Stable Diffusion (NO StreamDiffusion)
This version works WITHOUT StreamDiffusion library - just pure Stable Diffusion
"""
import os
import io
import base64
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import time
import torch
from diffusers import StableDiffusionImg2ImgPipeline, AutoencoderTiny
import threading
import queue

app = Flask(__name__)
CORS(app)

# Global state
pipe = None
current_prompt = "digital art, detailed, vibrant colors"
latest_drawing = None
latest_output = None
generation_queue = queue.Queue(maxsize=1)
output_queue = queue.Queue(maxsize=1)


def initialize_pipeline():
    """Initialize Stable Diffusion pipeline"""
    global pipe

    print("=" * 60)
    print("Initialisation de Stable Diffusion (sans StreamDiffusion)")
    print("=" * 60)
    print("")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    if device == "cpu":
        print("ATTENTION: CPU détecté - génération TRÈS lente!")
    else:
        gpu_name = torch.cuda.get_device_name(0)
        print(f"GPU: {gpu_name}")

    print("")
    print("Téléchargement du modèle SD-Turbo...")
    print("Cela peut prendre 5-10 minutes la première fois...")
    print("")

    # Load SD-Turbo for fast inference
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        safety_checker=None,
    )

    if device == "cuda":
        pipe = pipe.to("cuda")

        # Use TinyVAE for faster decoding
        try:
            print("Chargement de TinyVAE pour accélérer...")
            tiny_vae = AutoencoderTiny.from_pretrained(
                "madebyollin/taesd",
                torch_dtype=torch.float16
            ).to("cuda")
            pipe.vae = tiny_vae
            print("TinyVAE chargé!")
        except Exception as e:
            print(f"TinyVAE non disponible: {e}")

    # Optimize
    pipe.set_progress_bar_config(disable=True)

    print("")
    print("=" * 60)
    print("Pipeline Stable Diffusion initialisé avec succès!")
    print("=" * 60)
    print("")


def generation_worker():
    """Background worker for image generation"""
    global pipe, generation_queue, output_queue, current_prompt

    while True:
        try:
            # Get input image from queue
            try:
                input_data = generation_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            image = input_data['image']
            prompt = input_data.get('prompt', current_prompt)

            # Generate
            with torch.no_grad():
                result = pipe(
                    prompt=prompt,
                    image=image,
                    strength=0.7,  # How much to transform
                    num_inference_steps=2,  # SD-Turbo works with 1-4 steps
                    guidance_scale=0.0,  # SD-Turbo doesn't need CFG
                ).images[0]

            # Put in output queue
            try:
                output_queue.put_nowait(result)
            except queue.Full:
                try:
                    output_queue.get_nowait()
                    output_queue.put_nowait(result)
                except:
                    pass

        except Exception as e:
            print(f"Error in generation: {e}")
            time.sleep(0.1)


def generate_frames():
    """Generator for MJPEG streaming"""
    global latest_output

    last_frame_time = time.time()

    while True:
        try:
            current_time = time.time()
            if current_time - last_frame_time < 0.1:
                time.sleep(0.01)
                continue

            # Try to get new output
            try:
                new_output = output_queue.get_nowait()
                latest_output = new_output
            except queue.Empty:
                pass

            if latest_output is None:
                # Send blank image
                blank = Image.new('RGB', (512, 512), color='black')
                img_byte_arr = io.BytesIO()
                blank.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
            else:
                # Send latest output
                img_byte_arr = io.BytesIO()
                latest_output.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)

            last_frame_time = current_time

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr.read() + b'\r\n')

        except Exception as e:
            print(f"Error in streaming: {e}")
            time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process incoming drawing frame"""
    global generation_queue, latest_drawing, current_prompt

    try:
        data = request.get_json()
        image_data = data.get('frame', '')

        # Decode base64
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Resize to 512x512
        if image.size != (512, 512):
            image = image.resize((512, 512), Image.Resampling.LANCZOS)

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        latest_drawing = image

        # Send to generation queue
        try:
            generation_queue.put_nowait({
                'image': image,
                'prompt': current_prompt
            })
        except queue.Full:
            try:
                generation_queue.get_nowait()
                generation_queue.put_nowait({
                    'image': image,
                    'prompt': current_prompt
                })
            except:
                pass

        return jsonify({
            'status': 'success',
            'message': 'Frame processed'
        })

    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/update_prompt', methods=['POST'])
def update_prompt():
    """Update the generation prompt"""
    global current_prompt, latest_drawing, generation_queue

    try:
        data = request.get_json()
        new_prompt = data.get('prompt', '')

        if new_prompt and new_prompt != current_prompt:
            current_prompt = new_prompt
            print(f"Nouveau prompt: {current_prompt}")

            # Re-process latest drawing with new prompt
            if latest_drawing:
                try:
                    generation_queue.put_nowait({
                        'image': latest_drawing,
                        'prompt': current_prompt
                    })
                except queue.Full:
                    try:
                        generation_queue.get_nowait()
                        generation_queue.put_nowait({
                            'image': latest_drawing,
                            'prompt': current_prompt
                        })
                    except:
                        pass

            return jsonify({
                'status': 'success',
                'prompt': current_prompt
            })
        else:
            return jsonify({
                'status': 'unchanged',
                'prompt': current_prompt
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/status')
def status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'model': 'Stable Diffusion Turbo (sans StreamDiffusion)',
        'current_prompt': current_prompt
    })


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('../frontend/draw2img', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend/draw2img', path)


if __name__ == '__main__':
    print("=" * 60)
    print("Serveur Drawing-to-Image avec Stable Diffusion")
    print("(Version sans StreamDiffusion - plus compatible)")
    print("=" * 60)
    print("")

    # Initialize pipeline
    initialize_pipeline()

    # Start generation worker thread
    worker_thread = threading.Thread(target=generation_worker, daemon=True)
    worker_thread.start()
    print("Worker de génération démarré")

    print("")
    print("=" * 60)
    print("Serveur prêt!")
    print("Ouvrez http://localhost:5002 dans votre navigateur")
    print("=" * 60)
    print("")

    # Start Flask server
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
