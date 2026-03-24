# It sends requests to your FastAPI backend (upload PDFs + ask questions).

import requests # requests → used to call APIs (send HTTP requests)
from config import API_URL


def upload_pdfs_api(files):
    files_payload=[ ("files",(f.name,f.read(),"application/pdf")) for f in files]
    
    # Sends POST request to: http://localhost:8000/upload_pdfs/
    return requests.post(f"{API_URL}/upload_pdfs/",files=files_payload)

def ask_question(question):
    return requests.post(f"{API_URL}/ask/",data={"question":question})