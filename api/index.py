from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API is running"})

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(text)

        if hasattr(response, 'text') and response.text:
            return jsonify({"summary": response.text.strip()})
        else:
            return jsonify({"error": "No summary returned from Gemini"}), 502

    except Exception as e:
        return jsonify({"error": f"Gemini API failed: {str(e)}"}), 500

# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)
