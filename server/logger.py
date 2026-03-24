# We use logger to track what our program is doing and to find errors easily.

import logging

def setup_logger(name="MedicalAssistant"):
    logger = logging.getLogger(name)    # Creates (or gets existing) logger with name
    logger.setLevel(logging.DEBUG)      # Allow ALL logs (DEBUG → CRITICAL)

    ch = logging.StreamHandler()     # StreamHandler = print logs to console (terminal)
    ch.setLevel(logging.DEBUG)      # This handler will also allow all logs.

    formatter=logging.Formatter("[%(asctime)s] [%(levelname)s] --- [%(message)s]")
    ch.setFormatter(formatter)

    # Avoid Duplicate Logs
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


logger=setup_logger()

logger.info("RAG process started")
logger.debug("Debugging")
logger.error("Failed to load")
logger.critical("Critical message")