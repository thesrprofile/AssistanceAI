from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Hugging Face API settings
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # Open-source LLM
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    bot_response = query_hf(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)