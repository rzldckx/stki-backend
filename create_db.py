import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

data_file = os.getenv('DATA_FILE')
db_url = os.getenv('DB_URL')

# Load CSV data
df = pd.read_csv(data_file)

# Create PostgreSQL connection
engine = create_engine(db_url)
df.to_sql('news', engine, if_exists='replace', index=False)
print("PostgreSQL database setup completed successfully.")