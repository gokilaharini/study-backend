from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])
# Gemini API setup
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

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize this: {text}")

        return jsonify({"summary": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        # 
        # chat_model = genai.GenerativeModel("gemini-1.5-flash")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"asnswer this question : {user_input}")

        return jsonify({
            "response": response.text.strip(),
            "history": [{"role": h.role, "parts": h.parts[0].text} for h in model.history]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)