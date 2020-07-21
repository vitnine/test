import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))