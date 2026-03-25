import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOADED_DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "uploaded_docs")

@router.get("/uploaded_files/")
def get_uploaded_files():
    """Returns the list of PDF filenames already saved in uploaded_docs."""
    try:
        if not os.path.exists(UPLOADED_DOCS_DIR):
            return {"files": []}
        files = [
            f for f in os.listdir(UPLOADED_DOCS_DIR)
            if f.lower().endswith(".pdf")
        ]
        return {"files": files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
