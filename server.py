#!/usr/bin/env python3
"""
AI Drawing to Art - Backend Proxy Server
This server acts as a proxy to bypass CORS restrictions when calling AI APIs
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
import base64
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/generate'):
            self.handle_generate()
        else:
            SimpleHTTPRequestHandler.do_POST(self)

    def handle_generate(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            provider = data.get('provider')
            api_key = data.get('apiKey')
            prompt = data.get('prompt', '')
            image_data = data.get('imageData')  # base64 encoded

            if not api_key:
                self.send_error_response(400, 'API key is required')
                return

            if not image_data:
                self.send_error_response(400, 'Image data is required')
                return

            # Route to appropriate provider
            if provider == 'huggingface':
                result = self.call_huggingface(api_key, prompt, image_data)
            elif provider == 'openai':
                result = self.call_openai(api_key, prompt, image_data)
            elif provider == 'stability':
                result = self.call_stability(api_key, prompt, image_data)
            else:
                self.send_error_response(400, f'Unknown provider: {provider}')
                return

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            self.send_error_response(500, str(e))

    def call_huggingface(self, api_key, prompt, image_data):
        """Call Hugging Face API using new router endpoint"""
        # Using the new router endpoint (required as of 2024)
        url = 'https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell'

        # Create a descriptive prompt from user's input
        full_prompt = prompt or 'beautiful artwork, vibrant colors, artistic style, detailed, high quality'

        payload = {
            'inputs': full_prompt,
        }

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                image_bytes = response.read()

                # Check if the response is JSON (error or loading message)
                try:
                    response_text = image_bytes.decode('utf-8')
                    response_json = json.loads(response_text)

                    # Check if model is loading
                    if 'error' in response_json:
                        if 'loading' in response_json['error'].lower():
                            raise Exception('Model is loading. Please wait 20 seconds and try again.')
                        else:
                            raise Exception(f"API Error: {response_json['error']}")

                    # If we get here, it's an unexpected JSON response
                    raise Exception(f"Unexpected response: {response_text[:200]}")

                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Response is binary (image), which is what we want
                    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                    return {'success': True, 'image': image_b64}

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                if 'error' in error_json:
                    raise Exception(f"Hugging Face Error: {error_json['error']}")
            except json.JSONDecodeError:
                pass
            raise Exception(f'Hugging Face API Error ({e.code}): {error_body}')

    def call_openai(self, api_key, prompt, image_data):
        """Call OpenAI API"""
        # Note: This is simplified - you'd need to implement multipart/form-data
        raise Exception('OpenAI integration requires multipart form data - coming soon!')

    def call_stability(self, api_key, prompt, image_data):
        """Call Stability AI API"""
        raise Exception('Stability AI integration - coming soon!')

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        error = {'success': False, 'error': message}
        self.wfile.write(json.dumps(error).encode('utf-8'))

    def log_message(self, format, *args):
        # Custom log format
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)

    print("=" * 60)
    print("🎨 AI Drawing to Art Server")
    print("=" * 60)
    print(f"\n✅ Server running on: http://localhost:{port}")
    print(f"\n📱 Open this URL in your browser: http://localhost:{port}")
    print("\n💡 This server includes:")
    print("   - Web server for the app")
    print("   - Proxy server for AI APIs (no CORS issues!)")
    print("\n⏹️  Press Ctrl+C to stop")
    print("=" * 60)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)


if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)

    run_server(port)
