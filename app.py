from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from search import search_documents
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

db_url = os.getenv('DB_URL')

# Create PostgreSQL connection
engine = create_engine(db_url)

def get_news_data(page, per_page, category=None):
    offset = (page - 1) * per_page
    base_query = 'SELECT *, COUNT(*) OVER() AS total_count FROM news'
    
    if category:
        base_query += f" WHERE LOWER(category) = LOWER('{category}')"
    
    base_query += ' ORDER BY id'  # Pastikan untuk mengurutkan berdasarkan kolom yang sesuai
    base_query += f' LIMIT {per_page} OFFSET {offset}'
    
    with engine.connect() as conn:
        news_data = pd.read_sql_query(base_query, conn)
    
    total_results = int(news_data['total_count'][0]) if not news_data.empty else 0
    news_data.drop(columns=['total_count'], inplace=True)
    
    return news_data, total_results

@app.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', default=1, type=int)
    per_page = 12
    category = request.args.get('category', default=None, type=str)
    
    # Fetch news data with pagination and total count
    news_data, total_results = get_news_data(page, per_page, category)
    
    # Calculate total pages
    total_pages = (total_results + per_page - 1) // per_page
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total_results': total_results,
        'total_pages': total_pages,
        'news': news_data.to_dict(orient='records')
    })

@app.route('/news/<int:id>', methods=['GET'])
def get_news_by_id(id):
    query = 'SELECT * FROM news WHERE id = :id'
    
    with engine.connect() as conn:
        news_data = pd.read_sql_query(text(query), conn, params={'id': id})
    
    if news_data.empty:
        return jsonify({'error': 'News not found'}), 404
    
    return jsonify(news_data.to_dict(orient='records')[0])

@app.route('/search', methods=['GET'])
def search_news():
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=12, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    news_data, total_results = search_documents(query, page, per_page)
    
    # Calculate total pages
    total_pages = (total_results + per_page - 1) // per_page
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total_results': total_results,
        'total_pages': total_pages,
        'news': news_data.to_dict(orient='records')
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)