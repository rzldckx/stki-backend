from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_URL')
engine = create_engine(db_url)


def search_documents(query_string, page, per_page):
    """
    Fungsi untuk mencari dokumen dalam database PostgreSQL berdasarkan query_string.

    Parameters:
    query_string (str): Kata kunci pencarian.
    page (int): Nomor halaman untuk pagination.
    per_page (int): Jumlah hasil per halaman.

    Returns:
    pd.DataFrame: DataFrame yang berisi hasil pencarian.
    int: Total jumlah hasil pencarian.
    """
    offset = (page - 1) * per_page

    # Gunakan PostgreSQL untuk mencari dokumen dengan pencarian teks biasa
    search_query = text("""
        SELECT *, COUNT(*) OVER() AS total_count
        FROM news
        WHERE content ILIKE :query_string
        ORDER BY id
        LIMIT :per_page OFFSET :offset
    """)

    with engine.connect() as conn:
        news_data = pd.read_sql_query(search_query, conn, params={
            'query_string': f'%{query_string}%',
            'per_page': per_page,
            'offset': offset
        })

    total_results = int(news_data['total_count']
                        [0]) if not news_data.empty else 0
    news_data.drop(columns=['total_count'], inplace=True)

    return news_data, total_results
