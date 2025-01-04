from app import app
import setup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jalankan setup
setup.run_setup()

# Import aplikasi Flask setelah setup selesai

if __name__ == "__main__":
    # Gunakan port dari variabel lingkungan
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
