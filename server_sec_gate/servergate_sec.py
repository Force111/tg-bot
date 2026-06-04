import os
import logging
import sys
import json

REQUIRED_ENV_VARS = ["MONGO_URI", "TELEGRAM_KEY","GEMINI_API_KEY","DB_NAME","ADMIN_ID"]

for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logging.error(f"Environment variable '{var}' is not set")
        sys.exit(1)

def error_exit(message: str) -> None:
    print(f"Deployment was rejected: {message}")
    logging.error(f"Reason: {message}")
    sys.exit(1)

