import pandas as pd
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import shutil

# Load environment variables from .env file
load_dotenv()

# Define the schema
desired_schema = Schema(
    id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

def clear_index(index_dir):
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir)

# Clear the index directory before re-indexing
index_dir = os.getenv('INDEX_DIR')
clear_index(index_dir)

# Create or open the index
ix = create_in(index_dir, desired_schema)

# Create PostgreSQL connection
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

def add_documents(documents):
    writer = ix.writer()
    for doc_id, title, content in documents:
        writer.add_document(id=doc_id, title=title, content=content)
    writer.commit()

def index_db():
    with engine.connect() as conn:
        df = pd.read_sql_query('SELECT * FROM news', conn)
    documents = [(str(row['id']), row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)

if __name__ == '__main__':
    index_db()
    print("Indexing completed.")