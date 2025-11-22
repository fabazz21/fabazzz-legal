# 🎨 AI Drawing to Art

Transform your sketches into beautiful AI-generated artwork in real-time!

## ⚠️ IMPORTANT: Run as Web Server

**You cannot open `index.html` directly in your browser!** You must run it through a web server to avoid CORS errors.

### Quick Start (Choose ONE method):

**🚀 Easiest: Use the Helper Script**

For Mac/Linux:
```bash
./start-server.sh
```

For Windows:
```
start-server.bat
```

The script will automatically detect and use Python, Node.js, or PHP!

---

**Manual Start:**

**Python** (Works on Mac/Linux/Windows):
```bash
# Navigate to the project folder, then run:
python -m http.server 8000
# Open browser to: http://localhost:8000
```

**Node.js**:
```bash
npx http-server -p 8000
# Open browser to: http://localhost:8000
```

**VS Code**:
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

**PHP**:
```bash
php -S localhost:8000
```

---

## ✨ Features

- **Intuitive Drawing Canvas**: Draw with your mouse, stylus, or touch screen
- **Rich Color Palette**: 18+ preset colors plus custom color picker
- **Adjustable Brush Sizes**: From fine details (1px) to bold strokes (50px)
- **Multiple AI Providers**: Support for Hugging Face, OpenAI, and Stability AI
- **Mobile-Friendly**: Works perfectly on tablets and phones
- **Real-time Preview**: See your drawing and AI-generated art side by side
- **Download Results**: Save your AI-generated artwork

## 🚀 How to Use (After Starting Server)

1. **Get an API Key**: Choose an AI provider and get your API key (see below)
2. **Start Drawing**: Use the color palette and brush tools to create your sketch
3. **Generate Art**: Enter your API key and click "Generate AI Art"
4. **Download**: Save your beautiful AI-generated artwork!

## 🔑 Getting API Keys

### Option 1: Hugging Face (Recommended - Free Tier Available)

1. Go to [Hugging Face](https://huggingface.co/)
2. Create a free account
3. Navigate to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
4. Click "New token" and create a token with read permissions
5. Copy your token and paste it in the app

**Pros**: Free tier available, good quality results

### Option 2: OpenAI DALL-E

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and add payment method
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy your key and paste it in the app

**Pros**: High-quality results, reliable service
**Cons**: Paid service (charges per image)

### Option 3: Stability AI

1. Go to [Stability AI](https://platform.stability.ai/)
2. Create an account
3. Navigate to [Account > API Keys](https://platform.stability.ai/account/keys)
4. Generate a new API key
5. Copy your key and paste it in the app

**Pros**: Excellent quality, stable diffusion models
**Cons**: Paid service

## 🎯 How to Use

1. **Select Your Color**
   - Click any color from the palette
   - Or use the custom color picker for unlimited colors

2. **Adjust Brush Size**
   - Use the slider to choose brush size (1-50px)
   - See a live preview of your brush

3. **Draw Your Sketch**
   - Click and drag on the canvas to draw
   - Use different colors and sizes for details
   - Click "Clear Canvas" to start over

4. **Configure AI Settings**
   - Select your preferred AI provider
   - Enter your API key
   - (Optional) Add a text prompt to guide the AI
     - Example: "make it look like a watercolor painting"
     - Example: "add vibrant colors and realistic details"

5. **Generate Art**
   - Click "Generate AI Art" button
   - Wait for the AI to process (usually 10-30 seconds)
   - See your artwork appear in the right panel

6. **Download**
   - Click "Download Art" to save your creation

## 💡 Tips for Best Results

- **Start Simple**: Begin with basic shapes and outlines
- **Use Contrast**: Dark outlines help the AI understand your drawing
- **Add Details**: Small details can guide the AI's interpretation
- **Experiment with Prompts**: Try different text prompts to get varied results
  - "oil painting style"
  - "vibrant anime art"
  - "photorealistic with dramatic lighting"
  - "watercolor painting, soft colors"
- **Color Matters**: The colors you use in your sketch influence the final result

## 📱 Device Compatibility

- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Tablets (iPad, Android tablets)
- ✅ Touch-screen laptops
- ✅ Mobile phones (with responsive design)

## 🛠️ Technical Details

- **Frontend**: Pure HTML5, CSS3, and Vanilla JavaScript
- **Canvas API**: HTML5 Canvas for drawing functionality
- **AI Integration**: RESTful API calls to AI providers
- **No Backend Required**: Runs entirely in the browser

## 🔒 Privacy & Security

- API keys are stored only in your browser session
- No data is sent to any server except the AI provider you choose
- Your drawings are processed client-side
- No tracking or analytics

## 🐛 Troubleshooting

### ⚠️ CORS Error / "Failed to fetch" (MOST COMMON!)
**Problem**: Browser shows CORS policy error or "Failed to fetch"

**Solution**: You're opening the file directly instead of through a web server!
- **DO NOT** double-click `index.html` to open it
- **DO** run a local server (see "Run as Web Server" section above)
- Quick fix: `python -m http.server 8000` then open `http://localhost:8000`

### "Please enter your API key" error
- Make sure you've entered a valid API key in the configuration section

### "API Error" message
- Check that your API key is correct
- Ensure you have sufficient credits/quota with your AI provider
- Try a different AI provider

### Drawing not showing
- Make sure you're clicking and dragging on the canvas
- Try increasing the brush size
- Check that you've selected a visible color (not white on white)

### AI generation is slow
- This is normal - AI generation can take 10-60 seconds
- Hugging Face free tier may be slower during peak times
- Consider upgrading to a paid tier for faster processing

### Mobile touch not working
- Make sure you're using a modern mobile browser
- Try refreshing the page
- Ensure JavaScript is enabled

## 🚀 Future Enhancements

Potential features for future versions:
- Save/load drawings
- Undo/redo functionality
- More brush types (spray, calligraphy, etc.)
- Layers support
- Gallery of generated artwork
- Batch processing
- Style presets
- Image upload to convert photos to art

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Enjoy creating beautiful AI art! 🎨✨**
