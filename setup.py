import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from search import index_db

# Load environment variables from .env file
load_dotenv()

data_file = os.getenv('DATA_FILE')
db_file = os.getenv('DB_FILE')

# Load CSV data
df = pd.read_csv(data_file)

# Create SQLite connection and write data to SQLite
conn = sqlite3.connect(db_file)
df.to_sql('news', conn, if_exists='replace', index=False)
conn.close()

# Indexing Whoosh
index_db(db_file)

print("Setup completed successfully.")