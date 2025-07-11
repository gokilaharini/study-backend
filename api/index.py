from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API is running"})

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([f"Summarize this: {text}"])

        # Extract text safely
        if hasattr(response, 'text') and response.text:
            return jsonify({"summary": response.text.strip()})
        else:
            return jsonify({"error": "Empty response from Gemini API"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([f"Answer this question: {user_input}"])

        if hasattr(response, 'text') and response.text:
            return jsonify({"response": response.text.strip()}), 200
        else:
            return jsonify({"error": "Empty response from Gemini API"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
