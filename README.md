# STKI Backend

Proyek ini adalah backend dan API untuk search engine sederhana yang dibangun dengan menggunakan Flask dan Whoosh. Pengguna dapat mencari kata kunci tertentu dalam dokumen berita yang telah terindeks. API ini memungkinkan Anda untuk melakukan pencarian dan mendapatkan hasil yang relevan dari dataset berita.

Repository ini berisi semua kode yang diperlukan untuk menjalankan backend dan API.

## Cara install

1. Clone repository

2. Install dependency

   ```
   pip install -r requirements.txt
   ```

3. Download dataset dari https://www.kaggle.com/datasets/iqbalmaulana/indonesian-news-dataset dan pindahkan file CSV ke `data/data.csv`

4. Buat file `.env` berdasarkan `.env.example` dan sesuaikan jika diperlukan

   ```
   cp .env.example .env
   ```

5. Jalankan aplikasi Flask

   ```
   python app.py
   ```

6. Akses API di `http://127.0.0.1:5000/news?page=1` untuk mendapatkan halaman pertama dari berita. Alamat IP menyesuaikan di mana server dijalankan.

## Pagination

API mendukung pagination, memperbolehkan mengambil 10 berita dalam satu halaman. Anda bisa menentukan nomor halaman dengan query string, misal `?page=2` untuk halaman kedua.

## Search

API juga mendukung pencarian berita berdasarkan kata kunci. Anda bisa menggunakan `/search` dengan query string `q` untuk melakukan pencarian. Contoh:

```
http://127.0.0.1:5000/search?q=keyword
```

## Struktur Proyek

```
stki-backend
├── data
│   ├── data.csv        # Dataset dari Kaggle
│   ├── news.csv        # Dataset berita yang sudah diolah
│   └── README.md       # Dokumentasi dataset
├── indexdir            # Direktori untuk indeks Whoosh
│   └── README.md       # Dokumentasi direktori indeks
├── app.py              # Entry point dari aplikasi
├── search.py           # Logika untuk pengindeksan dan pencarian dokumen│   
├── requirements.txt    # Dependency proyek
├── .env                # Environment variables
├── .env.example        # Contoh file environment variables
└── README.md           # Dokumentasi proyek
```
