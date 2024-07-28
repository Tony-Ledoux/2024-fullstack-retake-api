import os
from dotenv import load_dotenv
load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")

documentation_url = os.getenv("DOCS_URL", None)
