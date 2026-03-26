# 🩺 Medical AI Assistant

An AI-powered medical assistant that allows users to upload medical documents (PDFs) and ask questions based on their content. The system uses RAG (Retrieval-Augmented Generation) with vector search and large language models to provide accurate, context-based responses.

---

## 🚀 Features

* 📄 Upload medical PDFs and store chunks in Pinecone vector database
* 🔍 Semantic search using vector embeddings
* 🤖 AI-powered question answering via LLM
* 💬 Chat-based interface with persistent chat history (survives page reloads)
* 📂 Sidebar file manager — view all uploaded files
* 🗑️ Delete individual files from disk and remove their chunks from Pinecone
* ⬇️ Download full chat history as a `.txt` file
* 🧹 Clear chat history with one click
* 🔐 Secure API key handling with `.env`

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* LangChain
* Pinecone (Vector Database)
* Groq (LLM - LLaMA3)
* SentenceTransformers (`all-MiniLM-L6-v2`) — local embedding model, no API key needed

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
│   ├── upload_pdfs.py         # Upload PDFs → chunks → Pinecone
│   ├── ask_question.py        # Query LLM with context
│   ├── uploaded_files.py      # List uploaded files
│   ├── delete_file.py         # Delete file + Pinecone chunks
│── modules/
│   ├── load_vectorstore.py    # Embedding + Pinecone upsert pipeline
│   ├── llm.py                 # LLM setup (Groq)
│   ├── query_handlers.py      # RAG query logic
│── middlewares/
│   ├── exception_handlers.py
│── uploaded_docs/             # Saved PDF files

client/
│── app.py                     # Streamlit entry point
│── components/
│   ├── chatUI.py              # Chat interface
│   ├── upload.py              # Sidebar uploader + file manager
│   ├── history_download.py    # Download & clear chat history
│── utils/
│   ├── api.py                 # API call helpers
│   ├── chat_history.py        # Persist/load chat history (JSON)
│── chat_history.json          # Auto-generated on first message

.env
.gitignore
README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Shlok-Maktarpara-23/Medical-AI-Assistant.git
cd Medical-AI-Assistant
```

### 2️⃣ Create Environment (using uv)

```bash
uv venv
uv pip install -r server/requirements.txt
```

### 3️⃣ Setup Environment Variables

Create a `.env` file inside the `server/` folder:

```
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Create a `config.py` inside `client/`:

```python
API_URL = "http://localhost:8000"
```

### 4️⃣ Run Backend

```bash
cd server
uvicorn main:app --reload
```

### 5️⃣ Run Frontend

```bash
cd client
streamlit run app.py
```

---

## 🔄 How It Works

1. User uploads PDFs via the sidebar
2. Text is extracted and split into chunks
3. Chunks are converted to embeddings using `all-MiniLM-L6-v2`
4. Embeddings are stored in Pinecone with IDs like `filename-0`, `filename-1`, ...
5. User asks a question in the chat
6. Relevant chunks are retrieved via semantic search
7. LLM (LLaMA3 via Groq) generates an answer based on the retrieved context
8. Chat history is saved to `chat_history.json` and restored on page reload

---

## 🗑️ File Deletion

When a user deletes a file from the sidebar:
- The PDF is removed from `uploaded_docs/`
- All corresponding Pinecone vector chunks (matched by filename prefix) are deleted
- The sidebar list refreshes automatically

---
