
# AI ChatBot with Text + Image Generation

This is a simple AI chatbot built using:
- 🧠 Gemini API (for text generation)
- 🎨 Stability AI (for image generation)
- 🎤 Voice Input (SpeechRecognition JS API)
- 🗣️ Text-to-Speech (Browser TTS)
- 🌙 Dark Mode toggle

## Features
- Chat-style interface
- Image generation when prompt includes "image" or "generate"
- Download generated images
- Voice-to-text input
- Text-to-speech replies
- Chat history with UI memory
- Dark mode toggle

## Setup Instructions

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Set your API keys in `.env` file:

```
GEMINI_API_KEY=your_gemini_key_here
STABILITY_API_KEY=your_stability_key_here
```

3. Run the Flask server:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser.

---

Built by Selvakumar S 🚀
