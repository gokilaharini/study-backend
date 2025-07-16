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
        
        model = genai.GenerativeModel("gemini-2.0-flash")
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
        
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([f"Answer this question: {user_input}"])

        if hasattr(response, 'text') and response.text:
            return jsonify({"response": response.text.strip()}), 200
        else:
            return jsonify({"error": "Empty response from Gemini API"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "").strip()
        quiz_type = data.get("quiz_type", "").strip().lower()

        if not transcript or quiz_type not in ["mcq", "true/false"]:
            return jsonify({"error": "Invalid input. Provide 'transcript' and 'quiz_type' (mcq or true/false)."}), 400

        prompt = f"""
        Based on the following transcript, generate 5 {quiz_type.upper()} quiz questions.

        Each quiz item must be in the format:
        {{
          "id": string (unique, e.g., "q1", "q2", ...),
          "question": string,
          "options": string[] (for MCQ: 4 options, for True/False: ["True", "False"]),
          "correctAnswer": number (index in options array),
          "explanation": string
        }}

        Transcript:
        \"\"\"
        {transcript}
        \"\"\"

        Respond ONLY with a valid JSON array of 5 quiz objects.
        """
        model = genai.GenerativeModel("gemini-2.0-flash")
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)

        # Try parsing response
        import json
        quizzes = json.loads(response.text)

        # Basic structure validation
        if not isinstance(quizzes, list) or len(quizzes) != 5:
            raise ValueError("Unexpected response structure")

        return jsonify({"quizzes": quizzes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
