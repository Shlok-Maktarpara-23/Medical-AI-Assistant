# it takes a user question and returns an AI-generated answer using your stored PDF data.

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from sentence_transformers import SentenceTransformer  
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router=APIRouter()

# ✅ Load embedding model locally (same model as load_vectorstore.py — must match!)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # Converts text → vector numbers

@router.post("/ask/")
async def ask_question(question: str = Form(...)): # Form() tells FastAPI: This value will come from form-data (like HTML form / Postman form-data)
    try:
        logger.info(f"user query: {question}")

        # Embed model + Pinecone setup
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
        embedded_query = embed_model.encode(question).tolist()  # ✅ Convert question → vector

        # Search in Pinecone
        res = index.query(vector=embedded_query, top_k=6, include_metadata=True)
        # Finds top 6 similar chunks and Returns metadata (text, source, etc.)

        # Convert results → Documents(Converts Pinecone output into LangChain format)
        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]

        # Retriever is already done, just return these docs
        class SimpleRetriever(BaseRetriever):
            docs: List[Document] = Field(default_factory=list)  # ✅ fixed pydantic field
            tags: Optional[List[str]] = Field(default_factory=list) # for tracking/logging
            metadata: Optional[dict] = Field(default_factory=dict)  # metadata -> extra info

            # Converts Pinecone output into LangChain format
            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self.docs

        retriever = SimpleRetriever(docs=docs)  # ✅ pass docs as keyword argument
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("query successfull")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
# Example matches 
# res = {
#   "matches": [
#     {"metadata": {"text": "Diabetes is...", "source": "file1.pdf"}},
#     {"metadata": {"text": "Symptoms include...", "source": "file2.pdf"}}
#   ]
# }