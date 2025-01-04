from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
import pandas as pd
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

index_dir = "indexdir"

# Define the schema
desired_schema = Schema(
    id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

# Check if the index directory exists and contains the index
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

if not os.listdir(index_dir):
    # Create a new index if it doesn't exist
    ix = create_in(index_dir, desired_schema)
else:
    # Open the existing index
    ix = open_dir(index_dir)

# Create PostgreSQL connection
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

# Open the index
index_dir = os.getenv('INDEX_DIR')
ix = open_dir(index_dir)


def search_documents(query_string, page=1, per_page=10):
    offset = (page - 1) * per_page

    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query, limit=None)
        total_results = len(results)
        result_ids = [result['id']
                      for result in results[offset:offset + per_page]]

    if not result_ids:
        return pd.DataFrame(), total_results

    # Load the PostgreSQL database to match the ids
    query = text('SELECT * FROM news WHERE id IN :ids')
    with engine.connect() as conn:
        news_data = pd.read_sql_query(
            query, conn, params={'ids': tuple(result_ids)})

    return news_data, total_results
