import logging
from agent.config import LOG_PATH

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

def log_attempt(query, attempt_num, code, error):
    logging.info(f"\n--- Attempt {attempt_num} ---")
    logging.info(f"Query: {query}")
    logging.info(f"Generated Code:\n{code}")
    if error:
        logging.info(f"Error:\n{error}")
