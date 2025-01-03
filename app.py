from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load dataset
data_file = 'data/data.csv'
news_data = pd.read_csv(data_file)

@app.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_news = news_data[start:end].to_dict(orient='records')
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(news_data),
        'news': paginated_news
    })

if __name__ == '__main__':
    app.run(debug=True)