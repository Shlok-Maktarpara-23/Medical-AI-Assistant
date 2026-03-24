#  to handle all errors (exceptions) in one central place instead of writing try-catch everywhere.

from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger


async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request) # Send request to actual API (like /chat, /predict)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION") # Print error in console
        return JSONResponse(status_code=500,content={"error":str(exc)}) # Response sent to user
