"""
Flask server for real-time text-to-image generation
"""
import os
import io
import base64
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import time
from stream_engine import StreamDiffusionEngine, StreamGenerator

app = Flask(__name__)
CORS(app)

# Global engine instance
engine = None
generator = None
current_prompt = "a beautiful landscape"


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
        use_lcm_lora=False,  # SD-Turbo already has this
        device=device,
    )

    # Prepare with initial prompt
    engine.prepare(current_prompt)

    # Create stream generator
    generator = StreamGenerator(engine)
    generator.start()

    print("Text-to-Image server initialized!")


def generate_frames():
    """Generator function for MJPEG streaming"""
    global generator, current_prompt

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
                print(f"FPS: {fps:.2f}")
                fps_start = time.time()

            # Yield frame in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr.read() + b'\r\n')

        except Exception as e:
            print(f"Error in frame generation: {e}")
            time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/update_prompt', methods=['POST'])
def update_prompt():
    """Update the generation prompt"""
    global current_prompt, generator

    try:
        data = request.get_json()
        new_prompt = data.get('prompt', '')

        if new_prompt and new_prompt != current_prompt:
            current_prompt = new_prompt
            print(f"Updating prompt to: {current_prompt}")

            # Send new prompt to generator
            generator.send_prompt(current_prompt)

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


@app.route('/generate_single', methods=['POST'])
def generate_single():
    """Generate a single image and return as base64"""
    global engine

    try:
        data = request.get_json()
        prompt = data.get('prompt', current_prompt)

        # Generate image
        image = engine.generate_txt2img(prompt)

        if image is None:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate image'
            }), 500

        # Convert to base64
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_base64 = base64.b64encode(img_byte_arr.read()).decode('utf-8')

        return jsonify({
            'status': 'success',
            'image': f'data:image/png;base64,{img_base64}'
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
    return send_from_directory('../frontend/txt2img', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend/txt2img', path)


if __name__ == '__main__':
    print("Starting Text-to-Image StreamDiffusion Server...")
    print("This may take a few minutes to download models on first run...")

    # Initialize engine before starting server
    initialize_engine()

    # Start Flask server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
