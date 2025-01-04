from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from search import search_documents
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

db_file = os.getenv('DB_FILE')

def get_news_data():
    conn = sqlite3.connect(db_file)
    news_data = pd.read_sql_query('SELECT * FROM news', conn)
    conn.close()
    return news_data

@app.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get category from query parameters
    category = request.args.get('category', default=None, type=str)

    # Load dataset dynamically
    news_data = get_news_data()

    # Filter news data by category if provided
    if category:
        filtered_news = news_data[news_data['category'].str.lower() == category.lower()]
    else:
        filtered_news = news_data

    paginated_news = filtered_news[start:end].to_dict(orient='records')
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(filtered_news),
        'news': paginated_news
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    results = search_documents(query, db_file)
    total_results = len(results)
    paginated_results = results[start:end]

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': total_results,
        'news': paginated_results
    })

@app.route('/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    news_data = get_news_data()
    news_item = news_data[news_data['id'] == news_id]
    
    if not news_item.empty:
        return jsonify(news_item.iloc[0].to_dict())
    else:
        return jsonify({'error': 'News item not found'}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)