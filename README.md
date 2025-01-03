# STKI Backend

Repository ini adalah backend dan API menggunakan Flask yang mengambil berita dari dataset yang disimpan dalam file CSV.

## Cara install

1. Clone repository

2. Install dependency

   ```
   pip install -r requirements.txt
   ```

3. Download dataset dari https://www.kaggle.com/datasets/iqbalmaulana/indonesian-news-dataset dan pindahkan file CSV ke `data/data.csv`

4. Jalankan aplikasi Flask

   ```
   python app.py
   ```

5. Akses API di `http://127.0.0.1:5000/news?page=1` untuk mendapatkan halaman pertama dari berita

## Pagination

API mendukung pagination, memperbolehkan mengambil 10 berita dalam satu halaman. Anda bisa menentukan nomor halaman dengan query string, misal `?page=2` untuk halaman kedua.
