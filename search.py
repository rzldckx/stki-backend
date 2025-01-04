import pandas as pd
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from dotenv import load_dotenv
import shutil

# Load environment variables from .env file
load_dotenv()

# Define the schema for the index
desired_schema = Schema(id=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))

# Function to check if the current schema matches the desired schema
def schema_matches(index_dir, desired_schema):
    try:
        ix = open_dir(index_dir)
        current_schema = ix.schema
        return current_schema == desired_schema
    except:
        return False

# Remove all files in the index directory except README if schema does not match
index_dir = os.getenv('INDEX_DIR')
if os.path.exists(index_dir):
    if not schema_matches(index_dir, desired_schema):
        for filename in os.listdir(index_dir):
            if filename != 'README':
                file_path = os.path.join(index_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
else:
    os.mkdir(index_dir)

# Create or open the index
try:
    if not os.listdir(index_dir):
        ix = create_in(index_dir, desired_schema)
    else:
        ix = open_dir(index_dir)
except EmptyIndexError:
    ix = create_in(index_dir, desired_schema)

def add_documents(documents):
    writer = ix.writer()
    for doc_id, title, content in documents:
        writer.add_document(id=doc_id, title=title, content=content)
    writer.commit()

def index_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.head(1000) # Limit to 1000 documents for testing
    documents = [(str(row['id']), row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)

def search_documents(query_string, csv_file_path):
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query)
        result_ids = [result['id'] for result in results]

    # Load the CSV file to match the ids
    df = pd.read_csv(csv_file_path)
    matched_rows = df[df['id'].astype(str).isin(result_ids)]

    return matched_rows.to_dict(orient='records')