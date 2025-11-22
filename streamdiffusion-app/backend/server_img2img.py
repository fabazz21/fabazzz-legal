"""
Flask server for real-time image-to-image generation with webcam
"""
import os
import io
import base64
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import time
import numpy as np
from stream_engine import StreamDiffusionEngine, StreamGenerator

app = Flask(__name__)
CORS(app)

# Global engine instance
engine = None
generator = None
current_prompt = "anime style"
latest_input_frame = None


def initialize_engine():
    """Initialize the StreamDiffusion engine"""
    global engine, generator

    # Check for GPU
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    if device == "cpu":
        print("WARNING: Running on CPU will be very slow!")

    # Initialize engine
    engine = StreamDiffusionEngine(
        model_id=os.getenv("MODEL_ID", "stabilityai/sd-turbo"),
        use_tiny_vae=True,
        use_lcm_lora=False,
        device=device,
    )

    # Prepare with initial prompt
    engine.prepare(current_prompt)

    # Create stream generator
    generator = StreamGenerator(engine)
    generator.start()

    print("Image-to-Image server initialized!")


def generate_frames():
    """Generator function for MJPEG streaming of output"""
    global generator

    frame_count = 0
    fps_start = time.time()

    while True:
        try:
            # Get latest generated image
            image = generator.get_latest_image()

            if image is None:
                # If no new image, wait a bit
                time.sleep(0.01)
                continue

            # Convert PIL Image to JPEG bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)

            # Calculate FPS
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed = time.time() - fps_start
                fps = 30 / elapsed
                print(f"Output FPS: {fps:.2f}")
                fps_start = time.time()

            # Yield frame in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr.read() + b'\r\n')

        except Exception as e:
            print(f"Error in frame generation: {e}")
            time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route for generated output"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process incoming webcam frame"""
    global generator, current_prompt, latest_input_frame

    try:
        data = request.get_json()
        image_data = data.get('frame', '')

        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Resize to reasonable size (512x512 is common for SD)
        image = image.resize((512, 512), Image.Resampling.LANCZOS)

        latest_input_frame = image

        # Send to generator
        generator.send_image(image, current_prompt)

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
    global current_prompt, engine, latest_input_frame, generator

    try:
        data = request.get_json()
        new_prompt = data.get('prompt', '')

        if new_prompt and new_prompt != current_prompt:
            current_prompt = new_prompt
            print(f"Updating prompt to: {current_prompt}")

            # Re-prepare engine with new prompt
            engine.prepare(current_prompt)

            # If we have a latest frame, re-process it with new prompt
            if latest_input_frame:
                generator.send_image(latest_input_frame, current_prompt)

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
    import torch
    return jsonify({
        'status': 'running',
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'model': os.getenv("MODEL_ID", "stabilityai/sd-turbo"),
        'current_prompt': current_prompt
    })


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('../frontend/img2img', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend/img2img', path)


if __name__ == '__main__':
    print("Starting Image-to-Image StreamDiffusion Server...")
    print("This may take a few minutes to download models on first run...")

    # Initialize engine before starting server
    initialize_engine()

    # Start Flask server
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
