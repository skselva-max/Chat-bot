from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data["message"]
    chat_history = data.get("history", [])

    # Image generation handling
    if "image" in user_input.lower() or "generate" in user_input.lower():
        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image",
                headers={
                    "Authorization": f"Bearer {STABILITY_API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json={
                    "text_prompts": [{"text": user_input}],
                    "cfg_scale": 7,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                },
            )
            result = response.json()
            if "artifacts" in result and result["artifacts"]:
                base64_image = result["artifacts"][0].get("base64")
                if base64_image:
                    image_data_url = f"data:image/png;base64,{base64_image}"
                    return jsonify({"type": "image", "data": image_data_url})
            return jsonify({"type": "text", "data": "Image generation failed."})
        except Exception as e:
            return jsonify({"type": "text", "data": f"Image generation error: {str(e)}"})

    # Text generation with enforced Markdown formatting
    try:
        history_prompt = ""
        for turn in chat_history:
            role = "User" if turn["role"] == "user" else "Bot"
            history_prompt += f"{role}: {turn['content']}\n"

        final_prompt = f"""
Respond to the following user input using Markdown format. 
- For code, use proper fenced code blocks with syntax highlighting (like ```c). 
- For steps or logic, format each step as a bullet or numbered item. 
- Never generate the code as a paragraph.

{history_prompt}
User: {user_input}
Bot:
        """

        try:
            response = model.generate_content(final_prompt)
        except Exception as e:
            if "429" in str(e):
                time.sleep(13)
                response = model.generate_content(final_prompt)
            else:
                raise e

        return jsonify({"type": "text", "data": response.text})

    except Exception as e:
        return jsonify({"type": "text", "data": f"Gemini error: {str(e)}"})

if __name__ == "__main__":
    print("Gemini Key Loaded:", GEMINI_API_KEY is not None)
    print("Stability Key Loaded:", STABILITY_API_KEY is not None)
    app.run(debug=True)
