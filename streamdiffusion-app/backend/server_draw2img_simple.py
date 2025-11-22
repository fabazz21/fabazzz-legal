"""
Simple Drawing-to-Image server for TESTING
This version works WITHOUT StreamDiffusion - just to test the setup!
Uses simple image filters instead of AI
"""
import os
import io
import base64
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time

app = Flask(__name__)
CORS(app)

# Global state
current_style = "none"
latest_drawing = None
latest_output = None


def apply_simple_style(image, style):
    """Apply simple image filters (no AI needed for testing)"""
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        if style == "blur":
            return image.filter(ImageFilter.GaussianBlur(radius=5))

        elif style == "sharpen":
            return image.filter(ImageFilter.SHARPEN)

        elif style == "edge":
            return image.filter(ImageFilter.FIND_EDGES)

        elif style == "emboss":
            return image.filter(ImageFilter.EMBOSS)

        elif style == "contour":
            return image.filter(ImageFilter.CONTOUR)

        elif style == "vibrant":
            enhancer = ImageEnhance.Color(image)
            return enhancer.enhance(2.0)

        elif style == "dramatic":
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(2.0)

        elif style == "invert":
            return ImageOps.invert(image)

        else:  # none or unknown
            return image

    except Exception as e:
        print(f"Error applying style: {e}")
        return image


def generate_frames():
    """Generator function for MJPEG streaming"""
    global latest_output

    last_frame_time = time.time()

    while True:
        try:
            # Send frame every 100ms
            current_time = time.time()
            if current_time - last_frame_time < 0.1:
                time.sleep(0.01)
                continue

            if latest_output is None:
                # Send a blank image if no output yet
                blank = Image.new('RGB', (512, 512), color='black')
                img_byte_arr = io.BytesIO()
                blank.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
            else:
                # Convert PIL Image to JPEG bytes
                img_byte_arr = io.BytesIO()
                latest_output.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)

            last_frame_time = current_time

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


@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process incoming drawing frame"""
    global latest_drawing, latest_output, current_style

    try:
        data = request.get_json()
        image_data = data.get('frame', '')

        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Ensure correct size
        if image.size != (512, 512):
            image = image.resize((512, 512), Image.Resampling.LANCZOS)

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        latest_drawing = image

        # Apply current style
        latest_output = apply_simple_style(image, current_style)

        return jsonify({
            'status': 'success',
            'message': 'Frame processed'
        })

    except Exception as e:
        print(f"Error processing frame: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/update_prompt', methods=['POST'])
def update_prompt():
    """Update the style (using simple filters)"""
    global current_style, latest_drawing, latest_output

    try:
        data = request.get_json()
        prompt = data.get('prompt', '').lower()

        # Map prompts to simple styles
        style_map = {
            'blur': 'blur',
            'sharp': 'sharpen',
            'edge': 'edge',
            'emboss': 'emboss',
            'contour': 'contour',
            'vibrant': 'vibrant',
            'dramatic': 'dramatic',
            'invert': 'invert',
        }

        # Find matching style
        new_style = 'none'
        for key, value in style_map.items():
            if key in prompt:
                new_style = value
                break

        current_style = new_style
        print(f"Style changed to: {current_style}")

        # Re-process latest drawing if exists
        if latest_drawing:
            latest_output = apply_simple_style(latest_drawing, current_style)

        return jsonify({
            'status': 'success',
            'prompt': current_style
        })

    except Exception as e:
        print(f"Error updating prompt: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/status')
def status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'device': 'CPU (Simple Test Mode - No AI)',
        'model': 'Simple Filters (Testing)',
        'current_prompt': current_style,
        'mode': 'SIMPLE TEST MODE'
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
    print("=" * 50)
    print("SIMPLE DRAWING SERVER - TEST MODE")
    print("=" * 50)
    print("")
    print("This is a SIMPLIFIED version for testing!")
    print("No AI/StreamDiffusion needed - uses simple filters")
    print("")
    print("Available styles (type in prompt):")
    print("  - blur")
    print("  - sharp")
    print("  - edge")
    print("  - emboss")
    print("  - vibrant")
    print("  - dramatic")
    print("  - invert")
    print("")
    print("Starting server on http://localhost:5002")
    print("=" * 50)

    # Start Flask server
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
