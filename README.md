# 🎙️ AI Mock Interview App  

## 📌 Overview  
The **AI Mock Interview App** is a web-based application designed to simulate real-life job interviews using AI.  
It leverages **speech-to-text (STT), text-to-speech (TTS), natural language processing (NLP)**, and **vector databases** to create an interactive interview experience.  

Users can:  
✅ Speak or type responses during the interview  
✅ Interact with a **virtual avatar** for a realistic experience  
✅ Store and retrieve past conversations for analysis  
✅ Run the app using **Docker and Azure**  

---

## 🚀 Features  
- **Speech-to-Text (STT):** Converts spoken words into text using **Azure Cognitive Services**  
- **Text-to-Speech (TTS):** AI responses are spoken out loud using **Azure TTS**  
- **Real-time AI Responses:** Uses **DeepSeek LLM via OpenRouter**  
- **Cloud Deployment:** Supports **Docker Compose** & **Azure App Service**  

---

## 🛠️ Tech Stack  
| Technology  | Purpose  |
|-------------|----------|
| **Flask**  | Backend API & routing  |
| **JavaScript (Vanilla + Fetch API)** | Frontend interaction |
| **Azure STT & TTS**  | Speech processing  |
| **DeepSeek via OpenRouter**  | AI-generated interview responses  |
| **Langfuse**  | LLM Monitoring |
| **Pinecone**  | Storing conversations & embeddings  |
| **Docker & Azure**  | Deployment & scalability  |

---

## ⚙️ Installation  

### **🔹 Prerequisites**  
Ensure you have the following installed:  
- Python 3.12+  
- Docker & Docker Compose  

### **🔹 Setup Steps**  

#### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/your-repo.git
cd your-repo

#### Set Up Environment Variables

Create a .env file in the root directory and add:

AZURE_KEY=your-azure-api-key
OPEN_ROUTER_AI_KEY=your-openrouter-key
PINECONE_API_KEY=your-pinecone-api-key  # If using Pinecone

#### Install Requirements
pip install -r requirements.txt

#### Run App or use Docker
python app.py

docker-compose up --build
