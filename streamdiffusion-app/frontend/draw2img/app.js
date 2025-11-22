// StreamDiffusion Drawing-to-Image Frontend
const API_URL = 'http://localhost:5002';

class Draw2ImgApp {
    constructor() {
        this.canvas = document.getElementById('drawingCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.outputStream = document.getElementById('outputStream');
        this.promptInput = document.getElementById('prompt');

        // Drawing state
        this.isDrawing = false;
        this.currentColor = '#000000';
        this.brushSize = 5;
        this.drawingHistory = [];
        this.hasDrawn = false;

        // Streaming state
        this.sendInterval = null;
        this.fpsCounter = 0;

        this.init();
    }

    init() {
        // Initialize canvas
        this.clearCanvas();

        // Drawing event listeners
        this.canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
        this.canvas.addEventListener('mousemove', (e) => this.draw(e));
        this.canvas.addEventListener('mouseup', () => this.stopDrawing());
        this.canvas.addEventListener('mouseout', () => this.stopDrawing());

        // Touch support
        this.canvas.addEventListener('touchstart', (e) => this.handleTouch(e, 'start'));
        this.canvas.addEventListener('touchmove', (e) => this.handleTouch(e, 'move'));
        this.canvas.addEventListener('touchend', () => this.stopDrawing());

        // Tool controls
        document.getElementById('brushSize').addEventListener('input', (e) => {
            this.brushSize = e.target.value;
            document.getElementById('brushSizeValue').textContent = e.target.value;
        });

        document.getElementById('customColor').addEventListener('input', (e) => {
            this.setColor(e.target.value);
        });

        // Color palette
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const color = btn.dataset.color;
                this.setColor(color);
                document.getElementById('customColor').value = color;
            });
        });

        // Action buttons
        document.getElementById('clearBtn').addEventListener('click', () => this.clearCanvas());
        document.getElementById('undoBtn').addEventListener('click', () => this.undo());
        document.getElementById('updateBtn').addEventListener('click', () => this.updatePrompt());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveImage());

        // Style buttons
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.dataset.prompt;
                this.promptInput.value = prompt;
                this.updatePrompt();
            });
        });

        // Template buttons
        document.querySelectorAll('.template-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.loadTemplate(btn.dataset.template);
            });
        });

        // Check server status
        this.checkStatus();

        // Start output stream
        this.startOutputStream();

        // Start sending frames
        this.startSendingFrames();

        // Update FPS counter
        setInterval(() => this.updateFPS(), 1000);
    }

    setColor(color) {
        this.currentColor = color;
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.color === color);
        });
    }

    startDrawing(e) {
        this.isDrawing = true;
        this.hasDrawn = true;

        // Hide overlay on first draw
        document.getElementById('canvasOverlay').classList.add('hidden');

        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);

        this.ctx.beginPath();
        this.ctx.moveTo(x, y);

        // Save state for undo
        this.saveState();
    }

    draw(e) {
        if (!this.isDrawing) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);

        this.ctx.lineWidth = this.brushSize;
        this.ctx.lineCap = 'round';
        this.ctx.strokeStyle = this.currentColor;
        this.ctx.lineTo(x, y);
        this.ctx.stroke();
    }

    stopDrawing() {
        this.isDrawing = false;
        this.ctx.beginPath();
    }

    handleTouch(e, type) {
        e.preventDefault();
        const touch = e.touches[0];
        if (!touch) return;

        const mouseEvent = new MouseEvent(
            type === 'start' ? 'mousedown' : 'mousemove',
            {
                clientX: touch.clientX,
                clientY: touch.clientY
            }
        );

        this.canvas.dispatchEvent(mouseEvent);
    }

    clearCanvas() {
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawingHistory = [];
        this.hasDrawn = false;
        document.getElementById('canvasOverlay').classList.remove('hidden');
    }

    saveState() {
        // Limit history to last 20 states
        if (this.drawingHistory.length > 20) {
            this.drawingHistory.shift();
        }
        this.drawingHistory.push(this.canvas.toDataURL());
    }

    undo() {
        if (this.drawingHistory.length > 0) {
            this.drawingHistory.pop();

            if (this.drawingHistory.length > 0) {
                const img = new Image();
                img.src = this.drawingHistory[this.drawingHistory.length - 1];
                img.onload = () => {
                    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                    this.ctx.drawImage(img, 0, 0);
                };
            } else {
                this.clearCanvas();
            }
        }
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
                    document.getElementById('loadingOverlay').classList.add('hidden');
                }, 2000);
            }
        } catch (error) {
            console.error('Error checking status:', error);
            document.getElementById('serverStatus').textContent = 'Error';
        }
    }

    startOutputStream() {
        this.outputStream.src = `${API_URL}/video_feed?t=${Date.now()}`;

        this.outputStream.onload = () => {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay && !overlay.classList.contains('hidden')) {
                overlay.classList.add('hidden');
            }
        };

        this.outputStream.onerror = () => {
            console.error('Output stream error, reconnecting...');
            setTimeout(() => {
                this.outputStream.src = `${API_URL}/video_feed?t=${Date.now()}`;
            }, 3000);
        };
    }

    startSendingFrames() {
        // Send frames at ~10 FPS
        const frameRate = 10;
        this.sendInterval = setInterval(() => {
            if (this.hasDrawn) {
                this.sendFrame();
            }
        }, 1000 / frameRate);
    }

    async sendFrame() {
        try {
            const frameData = this.canvas.toDataURL('image/jpeg', 0.8);

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

    async updatePrompt() {
        const prompt = this.promptInput.value.trim();

        if (!prompt) {
            alert('Please enter a style prompt!');
            return;
        }

        try {
            const updateBtn = document.getElementById('updateBtn');
            updateBtn.textContent = 'Applying...';
            updateBtn.disabled = true;

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

                updateBtn.textContent = '✓ Applied!';
                setTimeout(() => {
                    updateBtn.textContent = 'Apply Style';
                    updateBtn.disabled = false;
                }, 1500);
            } else {
                throw new Error(data.message || 'Failed to update prompt');
            }
        } catch (error) {
            console.error('Error updating prompt:', error);
            alert('Failed to update prompt: ' + error.message);
            document.getElementById('updateBtn').textContent = 'Apply Style';
            document.getElementById('updateBtn').disabled = false;
        }
    }

    loadTemplate(template) {
        // Simple template hints (you can expand this)
        const hints = {
            face: 'Draw a simple face outline with eyes, nose, and mouth',
            landscape: 'Draw hills, sun, trees, and clouds',
            portrait: 'Draw head and shoulders outline',
            abstract: 'Draw random shapes and lines'
        };

        alert(`Template: ${template}\n\nTip: ${hints[template]}`);
        this.clearCanvas();
    }

    saveImage() {
        // Download the current output
        const link = document.createElement('a');
        link.download = `streamdiffusion-${Date.now()}.png`;
        link.href = this.outputStream.src;
        link.click();
    }

    updateFPS() {
        const fps = this.fpsCounter;
        this.fpsCounter = 0;
        document.getElementById('fpsStatus').textContent = fps;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Draw2ImgApp();
});
