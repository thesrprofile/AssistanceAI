from flask import Flask, request, jsonify, render_template
import requests
import time
from urllib.parse import unquote

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")  
MODEL_NAME = "meta-llama/Llama-3.2-1B"  
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

POLITICAL_FIGURES = {
    "narendra modi": "Prime Minister of India (2014-present)",
    "modi": "Prime Minister of India (2014-present)",
}

PERSONAL_INFO = {
    "shashi ranjan kumar singh": {
        "introduction": "Shashi Ranjan Kumar Singh is a visionary AI Engineer, Data Scientist, and AI Consultant who has continuously pushed the boundaries of technology in AI, ML, and data-driven innovations.",
        "current_role": "AI Engineer at Outlier AI (Part Time)",
        "expertise": [
            "Machine Learning", "Deep Learning", "NLP", 
            "AI-driven solutions", "Python", "SQL", "OpenCV", 
            "LangChain", "LLMs", "TensorFlow", "Keras"
        ],
        "projects": [
            "Conversational AI Chatbot using open-source LLM and TensorFlow",
            "Language Detection System with 95% accuracy",
            "Power BI Dashboard for Business Insights"
        ],
        "links": {
            "linkedin": "https://linkedin.com/in/thesrprofile",
            "github": "https://github.com/thesrprofile",
            "email": "ai.shashiranjan@gmail.com"
        },
        "aspirations": "Expanding into React Native development while preparing for SSC CGL exam and seeking AI/Data Science opportunities in Noida."
    },
    "shashi": "Shashi Ranjan Kumar Singh is a visionary AI Engineer, Data Scientist, and AI Consultant who has continuously pushed the boundaries of technology in AI, ML, and data-driven innovations.",
    "thesrprofile": "This refers to Shashi Ranjan's online profiles (LinkedIn/Github). You can find more at: https://linkedin.com/in/thesrprofile or https://github.com/thesrprofile",
    "rajputai": "RajputAI is Shashi Ranjan's AI-related vlogging website where he shares knowledge about Artificial Intelligence.",
    "ai assistant": {
        "description": "Hello! I am your next-generation AI Assistant, designed and developed by Shashi Ranjan, a skilled AI Engineer and Data Scientist.",
        "capabilities": [
            "Answer questions with precision and context-awareness",
            "Assist in coding, debugging, and algorithm design",
            "Help with data analysis, visualization, and predictive modeling",
            "Generate creative content, summaries, and reports",
            "Automate repetitive tasks to boost productivity"
        ],
        "features": [
            "Fine-tuned for personalized, reliable, and insightful responses",
            "Incorporates advanced techniques like RAG (Retrieval-Augmented Generation)",
            "Built with ethical AI development principles",
            "Continuous improvement through real-time learning"
        ],
        "creator_vision": "Shashi believes in making AI accessible, helpful, and transformative for everyone. This assistant represents his vision for a smarter future where AI is a partner in progress.",
        "quote": "AI is not just a tool; it's a partner in progress. - Shashi Ranjan"
    },
    "who created you": "I was created by Shashi Ranjan Kumar Singh, He  is an AI Engineer and Data Scientist passionate about building intelligent systems that help people.",
    "who made you": "I was developed by Shashi Ranjan, who specializes in AI and machine learning. He designed me to be helpful, knowledgeable, and continuously improving."
}

def get_neutral_response(figure_name):
    """Generate neutral response about political figures"""
    figure_info = POLITICAL_FIGURES.get(figure_name.lower(), "")
    return (
        f"As an AI assistant, I maintain neutral perspective. {figure_info}. "
        "Different viewpoints exist about this leader: some emphasize development "
        "initiatives while others focus on social policies. For comprehensive "
        "understanding, I recommend checking multiple factual news sources."
    )

def get_personal_response(query):
    """Generate response about Shashi Ranjan or the AI assistant"""
    query = query.lower()
    if query in PERSONAL_INFO:
        info = PERSONAL_INFO[query]
        if isinstance(info, dict):
            if query == "ai assistant":
                response = f"{info['description']}\n\n"
                response += "🌟 <b>My Capabilities:</b>\n"
                response += "\n".join(f"- {cap}" for cap in info['capabilities']) + "\n\n"
                response += "🚀 <b>Special Features:</b>\n"
                response += "\n".join(f"- {feat}" for feat in info['features']) + "\n\n"
                response += f"💡 <b>Creator's Vision:</b>\n{info['creator_vision']}\n\n"
                response += f"\"{info['quote']}\""
                return response
            else:
                response = f"{info['introduction']}\n\nCurrent Role: {info['current_role']}\n\n"
                response += f"Expertise: {', '.join(info['expertise'][:5])}...\n\n"
                response += f"Notable Projects:\n- {info['projects'][0]}\n- {info['projects'][1]}\n\n"
                response += f"Connect:\nLinkedIn: {info['links']['linkedin']}\nGitHub: {info['links']['github']}"
                return response
        return info
    return None

def detect_political_question(text):
    """Check if question is about political figures"""
    text = unquote(text).lower()
    return any(figure in text for figure in POLITICAL_FIGURES.keys())

def detect_personal_question(text):
    """Check if question is about Shashi Ranjan or the AI assistant"""
    text = unquote(text).lower()
    query_terms = ["shashi", "shashi ranjan", "thesrprofile", "rajputai", 
                  "ai assistant", "your creator", "who made you", "who created you"]
    return any(term in text for term in query_terms)

def get_bot_response(payload, max_retries=3):
    """Handle API requests with retries"""
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if isinstance(response_data, list):
                return response_data[0].get('generated_text', '')
            return response_data.get('generated_text', '')
            
        except requests.exceptions.HTTPError as err:
            if response.status_code == 503:  # Model loading
                time.sleep(20)
                continue
            raise err
            
    return "I'm experiencing high load. Please try again later."

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Please enter a message', 'status': 'empty'})
    
    if detect_political_question(user_message):
        for figure in POLITICAL_FIGURES:
            if figure in user_message.lower():
                return jsonify({
                    'response': get_neutral_response(figure),
                    'status': 'neutral'
                })
    
    if detect_personal_question(user_message):
        for term in PERSONAL_INFO:
            if term in user_message.lower():
                response = get_personal_response(term)
                if response:
                    return jsonify({
                        'response': response,
                        'status': 'personal_info'
                    })
    
    payload = {
        "inputs": user_message,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.1,
            "return_full_text": False,
            "do_sample": True
        }
    }
    
    try:
        bot_response = get_bot_response(payload)
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'response': f"Error: {str(e)}",
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)