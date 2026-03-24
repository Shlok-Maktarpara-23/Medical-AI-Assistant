# 🩺 Medical AI Assistant

An AI-powered medical assistant that allows users to upload medical documents (PDFs) and ask questions based on their content. The system uses vector search and large language models to provide accurate, context-based responses.

---

## 🚀 Features

* 📄 Upload medical PDFs
* 🔍 Semantic search using vector embeddings
* 🤖 AI-powered question answering
* 💬 Chat-based interface (Streamlit)
* 📚 Source-based responses
* 🔐 Secure API key handling with `.env`

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* LangChain
* Pinecone (Vector Database)
* Groq (LLM - LLaMA3)
* Hugging Face Embedding Model 

### Frontend

* Streamlit

### Other Tools

* Python
* uv (environment & dependency management)

---

## 📂 Project Structure

```
server/
│── main.py
│── routes/
│   ├── upload_pdfs.py
│   ├── ask_question.py
│── modules/
│   ├── load_vectorstore.py
│   ├── llm.py
│   ├── query_handlers.py
│── middlewares/
│   ├── exception_handler.py

client/
│── ui/
│   ├── chat.py
│── utils/
│   ├── api.py

.env.example
.gitignore
README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/medical-ai-assistant.git
cd medical-ai-assistant
```

---

### 2️⃣ Create Environment (using uv)

```
uv venv
uv pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment Variables

Create `.env` file in root:

```
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medicalindex
API_URL=http://localhost:8000
```

---

### 4️⃣ Run Backend

```
cd server
uvicorn main:app --reload
```

---

### 5️⃣ Run Frontend

```
cd client
streamlit run app.py
```

---

## 🔄 How It Works

1. User uploads PDFs
2. Text is extracted and split into chunks
3. Chunks are converted into embeddings
4. Stored in Pinecone vector database
5. User asks a question
6. Relevant chunks are retrieved
7. LLM generates answer based on context

---
