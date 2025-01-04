import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

data_file = os.getenv('DATA_FILE')
db_file = os.getenv('DB_FILE')

# Load CSV data
df = pd.read_csv(data_file)

# Create SQLite connection
conn = sqlite3.connect(db_file)
df.to_sql('news', conn, if_exists='replace', index=False)
conn.close()