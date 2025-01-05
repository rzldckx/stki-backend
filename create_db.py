import pandas as pd
from sqlalchemy import create_engine, text
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

# Create index and tsvector column
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE news ADD COLUMN content_tsv tsvector;
        UPDATE news SET content_tsv = to_tsvector('simple', content);
        CREATE INDEX idx_news_content_tsv ON news USING gin (content_tsv);
        
        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
        ON news FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(content_tsv, 'pg_catalog.simple', content);
    """))

print("PostgreSQL database setup and indexing completed successfully.")
