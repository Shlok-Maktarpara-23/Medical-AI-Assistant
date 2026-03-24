# Accepting PDF files from the user → sending them to your vector database pipeline

from fastapi import APIRouter, UploadFile, File # UploadFile → Represents uploaded file from frontend
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router=APIRouter()

# API Endpoint
@router.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile] = File(...)):  # File → Tells FastAPI to expect files in request body
    try:
        logger.info("Recieved uploaded files")
        load_vectorstore(files)
        logger.info("Document added to vectorstore")
        return {"messages":"Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500,content={"error":str(e)}) 