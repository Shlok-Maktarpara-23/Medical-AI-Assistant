import os
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modules.load_vectorstore import index  # reuse the already-connected Pinecone index
from logger import logger

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploaded_docs")


@router.delete("/delete_file/{filename}")   # This tells FastAPI: "This function handles DELETE
def delete_file(filename: str):
    """
    1. Deletes the PDF from uploaded_docs/
    2. Deletes all Pinecone chunks whose IDs start with the file stem
       (e.g. "report" for "report.pdf" → deletes report-0, report-1, ...)
    """
    try:
        file_path = Path(UPLOAD_DIR) / filename
        stem = Path(filename).stem  # filename without extension

        # --- 1. Delete from Pinecone ---
        # index.list(prefix=...) returns an iterator of matching vector IDs
        ids_to_delete = []
        for id_batch in index.list(prefix=f"{stem}-"):
            ids_to_delete.extend(id_batch)

        if ids_to_delete:
            index.delete(ids=ids_to_delete)
            logger.info(f"Deleted {len(ids_to_delete)} chunks for '{filename}' from Pinecone")
        else:
            logger.warning(f"No Pinecone chunks found for stem '{stem}'")

        # --- 2. Delete file from disk ---
        if file_path.exists():
            os.remove(file_path)
            logger.info(f"Deleted file '{filename}' from uploaded_docs")
        else:
            logger.warning(f"File '{filename}' not found on disk")

        return {"message": f"'{filename}' and its {len(ids_to_delete)} chunks deleted successfully."}

    except Exception as e:
        logger.exception(f"Error deleting file '{filename}'")
        return JSONResponse(status_code=500, content={"error": str(e)})
