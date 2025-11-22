// StreamDiffusion Text-to-Image Frontend
const API_URL = 'http://localhost:5000';

class StreamDiffusionApp {
    constructor() {
        this.streamImage = document.getElementById('streamImage');
        this.promptInput = document.getElementById('prompt');
        this.updateBtn = document.getElementById('updateBtn');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.gridContainer = document.getElementById('gridContainer');

        this.savedImages = [];
        this.isStreaming = false;

        this.init();
    }

    init() {
        // Set up event listeners
        this.updateBtn.addEventListener('click', () => this.updatePrompt());
        this.promptInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.updatePrompt();
            }
        });

        // Quick prompt buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.dataset.prompt;
                this.promptInput.value = prompt;
                this.updatePrompt();
            });
        });

        // Check server status
        this.checkStatus();

        // Start video stream
        this.startStream();

        // Auto-save images periodically
        setInterval(() => this.captureCurrentImage(), 5000);
    }

    async checkStatus() {
        try {
            const response = await fetch(`${API_URL}/status`);
            const data = await response.json();

            document.getElementById('serverStatus').textContent = data.status;
            document.getElementById('deviceStatus').textContent = data.device.toUpperCase();
            document.getElementById('modelStatus').textContent = data.model.split('/').pop();
            document.getElementById('currentPrompt').textContent = data.current_prompt;

            // Hide loading overlay if server is ready
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

    startStream() {
        // Set up MJPEG stream
        this.streamImage.src = `${API_URL}/video_feed?t=${Date.now()}`;
        this.isStreaming = true;

        // Handle image load
        this.streamImage.onload = () => {
            if (this.loadingOverlay && !this.loadingOverlay.classList.contains('hidden')) {
                this.loadingOverlay.classList.add('hidden');
            }
        };

        // Handle errors
        this.streamImage.onerror = () => {
            console.error('Stream error, reconnecting...');
            setTimeout(() => {
                if (this.isStreaming) {
                    this.streamImage.src = `${API_URL}/video_feed?t=${Date.now()}`;
                }
            }, 3000);
        };
    }

    async updatePrompt() {
        const prompt = this.promptInput.value.trim();

        if (!prompt) {
            alert('Please enter a prompt!');
            return;
        }

        try {
            this.updateBtn.textContent = 'Updating...';
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

                // Show feedback
                this.updateBtn.textContent = '✓ Updated!';
                setTimeout(() => {
                    this.updateBtn.textContent = 'Generate';
                    this.updateBtn.disabled = false;
                }, 1500);
            } else {
                throw new Error(data.message || 'Failed to update prompt');
            }
        } catch (error) {
            console.error('Error updating prompt:', error);
            alert('Failed to update prompt: ' + error.message);
            this.updateBtn.textContent = 'Generate';
            this.updateBtn.disabled = false;
        }
    }

    captureCurrentImage() {
        // Capture current stream frame and add to grid
        if (!this.streamImage.src || this.streamImage.src.includes('video_feed')) {
            // Can't capture MJPEG stream directly, would need to implement server endpoint
            return;
        }

        const timestamp = new Date().toLocaleTimeString();
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item';
        gridItem.innerHTML = `
            <img src="${this.streamImage.src}" alt="Generated ${timestamp}">
            <div style="padding: 10px; font-size: 0.8em; color: #666;">
                ${timestamp}
            </div>
        `;

        // Remove the grid note if it exists
        const gridNote = this.gridContainer.querySelector('.grid-note');
        if (gridNote) {
            gridNote.remove();
        }

        // Add to beginning of grid
        this.gridContainer.insertBefore(gridItem, this.gridContainer.firstChild);

        // Limit to 12 images
        const items = this.gridContainer.querySelectorAll('.grid-item');
        if (items.length > 12) {
            items[items.length - 1].remove();
        }

        this.savedImages.push({
            timestamp,
            src: this.streamImage.src
        });
    }

    async generateSingle() {
        const prompt = this.promptInput.value.trim();

        if (!prompt) {
            alert('Please enter a prompt!');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/generate_single`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Display generated image
                const img = new Image();
                img.src = data.image;
                img.onload = () => {
                    this.streamImage.src = data.image;
                };
            } else {
                throw new Error(data.message || 'Failed to generate image');
            }
        } catch (error) {
            console.error('Error generating image:', error);
            alert('Failed to generate image: ' + error.message);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new StreamDiffusionApp();
});
