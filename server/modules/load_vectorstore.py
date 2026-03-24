# It Takes uploaded medical PDFs → splits them → converts to embeddings → stores in Pinecone
# (RAG Data Ingestion Pipeline)

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm  # tqdm → progress bar (UI improvement)
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer  # ✅ free, local, no API key needed

load_dotenv()

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
# database details
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="medicalindex"

# ✅ Load embedding model locally (no API key required)
# all-MiniLM-L6-v2 → lightweight, fast, 384 dimensions, great for semantic search
embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # Converts text → vector numbers

# Creates folder to store uploaded PDFs
UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

# initialize pinecone instance
pc=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(cloud="aws",region=PINECONE_ENV)
existing_indexes=[i["name"] for i in pc.list_indexes()]


if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,  # Size of embedding vector (all-MiniLM-L6-v2 produces 384 dimensions)
        metric="dotproduct",    # Used to compare similarity
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)   # Wait until index is ready

# Connect to index
index=pc.Index(PINECONE_INDEX_NAME) # Index = a place where all embeddings (vectors) are stored


# ✅ Embed a list of texts using sentence-transformers (runs locally, no API needed)
def embed_texts(texts):
    embeddings = embed_model.encode(texts, show_progress_bar=False)  # Converts text → vectors
    return embeddings.tolist()  # Convert numpy array → list for Pinecone


# load,split,embed and upsert pdf docs content

def load_vectorstore(uploaded_files):
    file_paths = []

    # 1. upload 
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename    # Save file in local folder
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()   # Extract text from PDF

        # 2. Split into Chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        # Extract: Text content, Metadata (page number etc.)
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [{**chunk.metadata, "text": chunk.page_content} for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        # 3. Embedding 
        print(f"🔍 Embedding {len(texts)} chunks...")
        embeddings = embed_texts(texts) # Converts text → vectors

        # 4. Upsert 
        print("📤 Uploading to Pinecone...")
        vectors = [
            {"id": id, "values": emb, "metadata": meta}  # Pinecone expects dict format
            for id, emb, meta in zip(ids, embeddings, metadatas)
        ]
        with tqdm(total=len(vectors), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=vectors)   # Upload vectors to Pinecone
            progress.update(len(vectors))

        print(f"✅ Upload complete for {file_path}")