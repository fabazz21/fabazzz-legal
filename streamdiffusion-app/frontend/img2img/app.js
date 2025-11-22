// StreamDiffusion Image-to-Image Frontend with Webcam
const API_URL = 'http://localhost:5001';

class Img2ImgApp {
    constructor() {
        this.webcam = document.getElementById('webcam');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.outputStream = document.getElementById('outputStream');
        this.promptInput = document.getElementById('prompt');

        this.startWebcamBtn = document.getElementById('startWebcamBtn');
        this.stopWebcamBtn = document.getElementById('stopWebcamBtn');
        this.updateBtn = document.getElementById('updateBtn');

        this.webcamOverlay = document.getElementById('webcamOverlay');
        this.loadingOverlay = document.getElementById('loadingOverlay');

        this.stream = null;
        this.isStreaming = false;
        this.sendInterval = null;
        this.fpsCounter = 0;
        this.lastFpsUpdate = Date.now();

        this.init();
    }

    init() {
        // Event listeners
        this.startWebcamBtn.addEventListener('click', () => this.startWebcam());
        this.stopWebcamBtn.addEventListener('click', () => this.stopWebcam());
        this.updateBtn.addEventListener('click', () => this.updatePrompt());

        // Quick style buttons
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.dataset.prompt;
                this.promptInput.value = prompt;
                this.updatePrompt();
            });
        });

        // Check server status
        this.checkStatus();

        // Start output stream
        this.startOutputStream();

        // Update FPS counter
        setInterval(() => this.updateFPS(), 1000);
    }

    async checkStatus() {
        try {
            const response = await fetch(`${API_URL}/status`);
            const data = await response.json();

            document.getElementById('serverStatus').textContent = data.status;
            document.getElementById('deviceStatus').textContent = data.device.toUpperCase();
            document.getElementById('currentPrompt').textContent = data.current_prompt;

            if (data.status === 'running') {
                setTimeout(() => {
                    this.loadingOverlay.classList.add('hidden');
                }, 2000);
            }
        } catch (error) {
            console.error('Error checking status:', error);
            document.getElementById('serverStatus').textContent = 'Error';
        }
    }

    async startWebcam() {
        try {
            // Request webcam access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            });

            this.webcam.srcObject = this.stream;
            this.isStreaming = true;

            // Update UI
            this.webcamOverlay.classList.add('hidden');
            this.startWebcamBtn.disabled = true;
            this.stopWebcamBtn.disabled = false;
            document.getElementById('webcamStatus').textContent = 'Running';

            // Wait for video to be ready
            this.webcam.onloadedmetadata = () => {
                // Set canvas size to match video
                this.canvas.width = this.webcam.videoWidth;
                this.canvas.height = this.webcam.videoHeight;

                // Start sending frames
                this.startSendingFrames();
            };

        } catch (error) {
            console.error('Error accessing webcam:', error);
            alert('Could not access webcam. Please ensure you have granted camera permissions.');
        }
    }

    stopWebcam() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        this.isStreaming = false;

        if (this.sendInterval) {
            clearInterval(this.sendInterval);
            this.sendInterval = null;
        }

        // Update UI
        this.webcamOverlay.classList.remove('hidden');
        this.startWebcamBtn.disabled = false;
        this.stopWebcamBtn.disabled = true;
        document.getElementById('webcamStatus').textContent = 'Stopped';
    }

    startSendingFrames() {
        // Send frames at ~15 FPS (to avoid overwhelming the server)
        const frameRate = 15;
        this.sendInterval = setInterval(() => {
            this.captureAndSendFrame();
        }, 1000 / frameRate);
    }

    async captureAndSendFrame() {
        if (!this.isStreaming || !this.webcam.readyState === 4) {
            return;
        }

        try {
            // Draw current video frame to canvas
            this.ctx.drawImage(this.webcam, 0, 0, this.canvas.width, this.canvas.height);

            // Convert to base64
            const frameData = this.canvas.toDataURL('image/jpeg', 0.8);

            // Send to server
            const response = await fetch(`${API_URL}/process_frame`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ frame: frameData }),
            });

            if (response.ok) {
                this.fpsCounter++;
            }

        } catch (error) {
            console.error('Error sending frame:', error);
        }
    }

    startOutputStream() {
        // Set up MJPEG stream for output
        this.outputStream.src = `${API_URL}/video_feed?t=${Date.now()}`;

        this.outputStream.onload = () => {
            if (this.loadingOverlay && !this.loadingOverlay.classList.contains('hidden')) {
                this.loadingOverlay.classList.add('hidden');
            }
        };

        this.outputStream.onerror = () => {
            console.error('Output stream error, reconnecting...');
            setTimeout(() => {
                this.outputStream.src = `${API_URL}/video_feed?t=${Date.now()}`;
            }, 3000);
        };
    }

    async updatePrompt() {
        const prompt = this.promptInput.value.trim();

        if (!prompt) {
            alert('Please enter a style prompt!');
            return;
        }

        try {
            this.updateBtn.textContent = 'Applying...';
            this.updateBtn.disabled = true;

            const response = await fetch(`${API_URL}/update_prompt`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            if (data.status === 'success' || data.status === 'unchanged') {
                document.getElementById('currentPrompt').textContent = data.prompt;

                this.updateBtn.textContent = '✓ Applied!';
                setTimeout(() => {
                    this.updateBtn.textContent = 'Apply Style';
                    this.updateBtn.disabled = false;
                }, 1500);
            } else {
                throw new Error(data.message || 'Failed to update prompt');
            }
        } catch (error) {
            console.error('Error updating prompt:', error);
            alert('Failed to update prompt: ' + error.message);
            this.updateBtn.textContent = 'Apply Style';
            this.updateBtn.disabled = false;
        }
    }

    updateFPS() {
        const fps = this.fpsCounter;
        this.fpsCounter = 0;
        document.getElementById('fpsStatus').textContent = fps;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Img2ImgApp();
});
