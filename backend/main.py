from dotenv import load_dotenv
import os

DB_USERNAME = os.getenv("DB_USERNAME")
load_dotenv()

print(DB_USERNAME);
