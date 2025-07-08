from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API is running"})


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Call Gemini API
        response = model.generate_content(text)

        # Return result
        if hasattr(response, 'text') and response.text:
            return jsonify({"summary": response.text.strip()})
        else:
            return jsonify({"error": "Empty response from Gemini"}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Required by Vercel
def handler(environ, start_response):
    return app(environ, start_response)
