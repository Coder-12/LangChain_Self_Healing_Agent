# agent/config.py

import os
from dotenv import load_dotenv

# Load .env file (OPENAI_API_KEY, etc.)
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_RETRIES = 3
MODEL_NAME = "gpt-4.1-mini"  # Change to gpt-4 if needed # gpt-4.1-mini
LOG_PATH = "logs/agent_logs.log"

# File paths
SCHEMA_CSV_PATH = "data/sample_df.csv"

# Schema column info (can also be loaded dynamically from DataFrame)
SCHEMA_DESCRIPTION = {
    "name": "Name of the person",
    "age": "Age in years",
    "city": "City of residence",
    "income": "Annual income in USD",
    "profession": "Job title or profession",
    "joined_date": "Date the person joined the company (YYYY-MM-DD)"
}
