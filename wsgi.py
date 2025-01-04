import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jalankan setup
import setup

# Import aplikasi Flask setelah setup selesai
from app import app

if __name__ == "__main__":
    app.run()