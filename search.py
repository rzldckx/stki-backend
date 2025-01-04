import pandas as pd
from whoosh.index import create_in, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from dotenv import load_dotenv
import shutil
import sqlite3

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
try:
    ix = create_in(index_dir, desired_schema)
except EmptyIndexError:
    ix = create_in(index_dir, desired_schema)

def add_documents(documents):
    writer = ix.writer()
    for doc_id, title, content in documents:
        writer.add_document(id=doc_id, title=title, content=content)
    writer.commit()

def index_db(db_file):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query('SELECT * FROM news', conn)
    df = df.head(5000) # Limit to 5000 documents for testing
    documents = [(str(row['id']), row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)
    conn.close()

def search_documents(query_string, db_file):
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query)
        result_ids = [result['id'] for result in results]

    # Load the SQLite database to match the ids
    conn = sqlite3.connect(db_file)
    query = 'SELECT * FROM news WHERE id IN ({})'.format(','.join('?' * len(result_ids)))
    df = pd.read_sql_query(query, conn, params=result_ids)
    conn.close()

    return df.to_dict(orient='records')