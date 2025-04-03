# **Assistance AI - Project Overview**  

🚀 **Assistance AI** is a **chatbot application** powered by **Hugging Face’s open-source LLM (Mistral-7B)** and deployed using **Flask & Render**. It provides **real-time AI-powered responses** in a simple, user-friendly web interface.  

---

## **📌 Key Features**  
✅ **Open-Source AI Model** – Uses `mistralai/Mistral-7B-Instruct-v0.1` from Hugging Face.  
✅ **Real-Time Chat Interface** – Send messages and get AI-generated responses instantly.  
✅ **Simple & Scalable Backend** – Built with **Flask** (Python) for easy modifications.  
✅ **Secure API Handling** – Uses `.env` to protect Hugging Face API keys.  
✅ **Production-Ready Deployment** – Hosted on **Render** with Gunicorn for reliability.  

---

## **🛠️ Tech Stack**  
| Category       | Technology Used |
|---------------|----------------|
| **Backend**   | Flask (Python) |
| **Frontend**  | HTML, CSS, JS |
| **AI Model**  | Hugging Face API (Mistral-7B) |
| **Deployment** | Render (Gunicorn) |
| **Security**  | `.env` for API keys |

---

## **📂 Project Structure**  
```
assistance-ai/
├── app.py              # Flask backend (handles API calls)
├── requirements.txt    # Python dependencies
├── .env                # Stores Hugging Face API key
└── templates/
    └── chat.html       # Frontend chat interface
```

---

## **🔧 How It Works**  
1. **User Input** → Message sent via frontend (HTML/JS).  
2. **Flask Backend** → Processes request & queries Hugging Face API.  
3. **AI Response** → Mistral-7B generates a reply.  
4. **Output** → Response displayed in the chatbox.  

---

## **🚀 Deployment**  
Hosted on **Render** using:  
- **Gunicorn** (Production WSGI Server)  
- **Hugging Face Inference API** (Free Tier)  

🔗 **Live Demo:** https://assistanceai.onrender.com/  

---

## **⚙️ Setup & Run Locally**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/assistance-ai.git
cd assistance-ai
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Add Hugging Face API Key**  
Create `.env` file:  
```env
HF_API_KEY="your_huggingface_api_token"
```

### **4. Run Flask App**  
```bash
python app.py
```
Visit → `http://localhost:5000`  

### **5. Deploy to Render**  
- Push to GitHub & connect to Render.  
- Set **Start Command:** `gunicorn app:app`  

---

## **📜 Future Improvements**  
🔹 **Add More Models** (e.g., Llama 3, GPT-2)  
🔹 **Streaming Responses** (Better UX)  
🔹 **User Authentication** (Optional)  
🔹 **Mobile App Integration** (Flutter/React Native)  

---

## **🙏 Credits**  
- **Hugging Face** for the open-source LLM API.  
- **Render** for free cloud hosting.  
- **Flask & Gunicorn** for backend stability.  

---

## **📄 License**  
MIT License - Free for personal & commercial use.  

---
