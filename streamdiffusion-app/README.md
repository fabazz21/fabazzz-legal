# 🎨 StreamDiffusion App

A real-time AI image generation application powered by [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion), featuring text-to-image, image-to-image (webcam), and **drawing-to-image** capabilities.

## ✨ Features

### Text-to-Image Generation
- **Real-time generation** - Watch images generate as you type
- **MJPEG streaming** - Smooth, continuous image updates
- **Quick prompts** - Pre-configured prompts for instant results
- **Grid gallery** - Auto-save generated images

### Image-to-Image with Webcam
- **Live webcam input** - Transform your camera feed in real-time
- **Style transfer** - Apply artistic styles to live video
- **Multiple presets** - Anime, oil painting, cyberpunk, and more
- **Interactive controls** - Adjust styles on-the-fly

### Drawing-to-Image Generation ⭐ NEW!
- **Interactive canvas** - Draw with mouse or touch
- **Real-time AI transformation** - Watch your sketches become art
- **Color palette** - 8 preset colors + custom picker
- **Brush controls** - Adjustable size and color
- **Style presets** - Photorealistic, anime, watercolor, and more
- **Undo/Clear** - Refine your drawings easily
- **Save output** - Download generated images

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (3.11 works too)
- **NVIDIA GPU** with CUDA support (recommended)
  - RTX 30/40 series recommended for best performance
  - Can run on CPU but will be very slow
- **6GB+ VRAM** recommended
- **10GB+ free disk space** (for models)

### Installation

#### Linux/Mac

```bash
# Clone or navigate to the project directory
cd streamdiffusion-app

# Run setup script
chmod +x setup.sh
./setup.sh
```

#### Windows

```cmd
# Run setup script
setup.bat
```

#### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install PyTorch with CUDA 11.8
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118

# Install dependencies
cd backend
pip install -r requirements.txt
```

## 🎮 Usage

### Text-to-Image Server

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start server
cd backend
python server_txt2img.py

# Open in browser
# http://localhost:5000
```

**Features:**
- Enter custom prompts or use quick presets
- Real-time image generation stream
- Auto-captured gallery of generations
- FPS monitoring

### Image-to-Image Server (Webcam)

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start server
cd backend
python server_img2img.py

# Open in browser
# http://localhost:5001
```

**Features:**
- Click "Start Webcam" to begin
- Choose style presets or custom prompts
- See your webcam transformed in real-time
- Switch styles on-the-fly

### Drawing-to-Image Server ⭐ NEW!

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start server
cd backend
python server_draw2img.py

# Open in browser
# http://localhost:5002
```

**Features:**
- Draw on interactive canvas with mouse/touch
- Choose colors and brush sizes
- Real-time AI transformation of your drawings
- 8 style presets (photorealistic, anime, watercolor, etc.)
- Undo/clear tools for easy editing
- Save generated images

**📖 Complete Tutorial:** See [TUTORIAL_DRAW2IMG.md](TUTORIAL_DRAW2IMG.md) for detailed guide!

## 📁 Project Structure

```
streamdiffusion-app/
├── backend/
│   ├── stream_engine.py      # Core StreamDiffusion engine
│   ├── server_txt2img.py     # Text-to-image Flask server
│   ├── server_img2img.py     # Image-to-image Flask server
│   ├── server_draw2img.py    # Drawing-to-image Flask server
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── txt2img/
│   │   ├── index.html        # Text-to-image UI
│   │   ├── style.css         # Styles
│   │   └── app.js            # Frontend logic
│   ├── img2img/
│   │   ├── index.html        # Image-to-image UI
│   │   ├── style.css         # Styles
│   │   └── app.js            # Webcam & streaming logic
│   └── draw2img/             # ⭐ NEW!
│       ├── index.html        # Drawing-to-image UI
│       ├── style.css         # Styles
│       └── app.js            # Canvas & drawing logic
├── assets/                   # Generated images/assets
├── setup.sh                  # Linux/Mac setup script
├── setup.bat                 # Windows setup script
├── run_txt2img.sh/.bat       # Quick-start scripts
├── run_img2img.sh/.bat
├── run_draw2img.sh/.bat      # ⭐ NEW!
├── README.md                 # This file
└── TUTORIAL_DRAW2IMG.md      # ⭐ Drawing tutorial
```

## ⚙️ Configuration

### Environment Variables

```bash
# Model selection (default: stabilityai/sd-turbo)
export MODEL_ID="stabilityai/sd-turbo"
# or: "runwayml/stable-diffusion-v1-5"
# or: any HuggingFace diffusion model

# Server port (default: 5000 for txt2img, 5001 for img2img)
export PORT=5000

# Hugging Face cache location
export HF_HOME=/path/to/cache
```

### Model Options

The app supports various Stable Diffusion models:

- **sd-turbo** (default) - Fast, optimized for real-time
- **stable-diffusion-v1-5** - Classic SD model
- **Any HuggingFace model** - Specify model ID

## 🎨 Prompt Tips

### For Best Results:

1. **Be descriptive**: "a beautiful landscape with mountains" → "a beautiful landscape with snow-capped mountains, golden sunset, vibrant colors, photorealistic"

2. **Include style keywords**:
   - "digital art"
   - "oil painting"
   - "photorealistic"
   - "anime style"
   - "cinematic"

3. **Add quality modifiers**:
   - "highly detailed"
   - "8k"
   - "professional"
   - "award winning"

### Example Prompts:

```
Text-to-Image:
- "a futuristic cityscape at night, neon lights, cyberpunk style, highly detailed"
- "cute cat wearing wizard hat, magical atmosphere, digital art, vibrant colors"
- "ancient temple in jungle, overgrown with vines, cinematic lighting, photorealistic"

Image-to-Image (Styles):
- "anime style, vibrant colors, studio ghibli"
- "oil painting, impressionist, brushstrokes visible"
- "cyberpunk, neon, futuristic, blade runner"
- "watercolor painting, soft colors, dreamy atmosphere"
```

## 🔧 Troubleshooting

### Issue: Slow generation / Low FPS

**Solutions:**
- Ensure you're using a CUDA-capable GPU
- Install xformers: `pip install xformers`
- Reduce image resolution in code
- Use SD-Turbo model (default)

### Issue: Out of memory errors

**Solutions:**
- Reduce batch size
- Use TinyVAE (enabled by default)
- Enable xformers
- Reduce image resolution

### Issue: Models not downloading

**Solutions:**
- Check internet connection
- Set HuggingFace token if needed: `huggingface-cli login`
- Manually download models to HF cache

### Issue: Webcam not working

**Solutions:**
- Grant browser camera permissions
- Check if camera is used by another app
- Try different browser (Chrome recommended)
- Check HTTPS/localhost permissions

## 📊 Performance

Expected performance on different hardware:

| GPU | Text-to-Image | Image-to-Image | Notes |
|-----|---------------|----------------|-------|
| RTX 4090 | 80-100 fps | 60-90 fps | Best performance |
| RTX 3090 | 60-80 fps | 40-60 fps | Great performance |
| RTX 3070 | 30-50 fps | 20-35 fps | Good performance |
| RTX 2060 | 15-25 fps | 10-20 fps | Acceptable |
| CPU Only | 0.5-2 fps | 0.3-1 fps | Not recommended |

*Performance varies based on prompt complexity and settings*

## 🛠️ Advanced Usage

### Running with TensorRT (For Maximum Speed)

```bash
# Install TensorRT dependencies
pip install tensorrt torch-tensorrt

# Modify server code to enable TensorRT
# (Requires additional setup - see StreamDiffusion docs)
```

### Custom Models

```python
# In stream_engine.py, change model_id:
engine = StreamDiffusionEngine(
    model_id="your-model-id-here",
    use_tiny_vae=True,
    use_lcm_lora=True,  # Enable for non-turbo models
)
```

### API Endpoints

Both servers expose these endpoints:

- `GET /` - Serve frontend
- `GET /video_feed` - MJPEG stream
- `POST /update_prompt` - Update generation prompt
- `GET /status` - Server status
- `POST /process_frame` - Process webcam frame (img2img only)

## 📝 License

This project uses StreamDiffusion, which is licensed under Apache 2.0. Please refer to individual model licenses for commercial use.

## 🙏 Acknowledgments

- [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion) - Core real-time diffusion pipeline
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) - Base diffusion models
- [Hugging Face](https://huggingface.co/) - Model hosting and diffusers library

## 🐛 Known Issues

- First generation may be slow (model loading)
- CPU mode is extremely slow
- High VRAM usage (6GB+ recommended)
- Browser compatibility varies (Chrome works best)

## 🚀 Future Improvements

- [ ] LoRA support
- [ ] ControlNet integration
- [ ] Multiple model switching
- [ ] Image upscaling
- [ ] Video recording
- [ ] Prompt history
- [ ] Settings panel
- [ ] Mobile optimization

## 💡 Tips

1. **First run**: Model download takes 5-10 minutes
2. **Best performance**: Use RTX 30/40 series GPU
3. **Webcam mode**: Good lighting improves results
4. **Prompts**: More specific = better results
5. **Styles**: Experiment with different art styles

## 📧 Support

For issues and questions:
1. Check troubleshooting section
2. Review StreamDiffusion documentation
3. Open an issue on GitHub

---

**Enjoy creating amazing AI art in real-time! 🎨✨**
