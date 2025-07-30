# AI Assistant untuk Release Notes SimpliDOTS

## Deskripsi

Sistem AI untuk memproses, meringkas, dan menyediakan antarmuka tanya-jawab interaktif untuk data *release notes* SimpliDOTS. Solusi ini dirancang untuk meningkatkan aksesibilitas dan pemahaman tim internal terhadap pembaruan produk.

Proyek ini merupakan submisi untuk *Technical Test AI Engineer Intern*.

---

## Fitur Utama

-   **Pemrosesan Data**: Melakukan *web scraping* dari sumber *release notes* dan menstrukturkan konten ke dalam format JSON (`simpli.json`) yang bersih dan siap diolah, lengkap dengan metadata.

-   **Ringkasan Otomatis**: Mengimplementasikan metode **"RAG-based Summarization"** yang efisien untuk menghasilkan ringkasan dari dokumen-dokumen paling relevan. Pendekatan ini meminimalisir latensi dan biaya komputasi.

-   **Chatbot RAG Interaktif**: Menyediakan antarmuka CLI untuk tanya-jawab yang didukung arsitektur **RAG (Retrieval-Augmented Generation)**. Fitur ini memastikan jawaban akurat dan mampu menangani pertanyaan berbasis waktu (contoh: "update minggu ini") melalui **"Query Transformation"**.

---

## Arsitektur & Teknologi

-   **Bahasa**: Python 3.9+
-   **Framework AI**: LangChain
-   **Model LLM**: Google Gemini (`gemini-1.5-flash-latest`)
-   **Model Embedding**: Google Generative AI Embeddings (`models/embedding-001`)
-   **Vector Database**: ChromaDB

---

## Panduan Eksekusi

### 1. Prasyarat

-   Python 3.9+
-   Google API Key (dapat diperoleh dari [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Instalasi

Clone repositori
```bash
git clone [URL_REPOSITORI_ANDA]
cd [NAMA_FOLDER_REPOSITORI]
```

Buat dan aktifkan virtual environment
```
python -m venv venv
source venv/bin/activate
```
Instal dependensi
```
pip install -r requirements.txt
```

### 3. Konfigurasi
Buat file .env dan isi dengan API KEY GOOGLE anda.
Isi file .env:
```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

### 4. Alur Eksekusi
Jalankan skrip berikut secara berurutan dari terminal.

a. Ekstraksi Data (Opsional)
Jika file simplidots.json belum ada, jalankan notebook scrape_release_notes_SimpliDOTS.ipynb untuk menghasilkan file data.

b. Pembangunan Vector Database (Hanya Sekali)
Perintah ini memproses simplidots.json dan membuat direktori chroma_db yang berisi database vektor.
```
python vectorDB.py
```

c. Pembuatan Ringkasan
Skrip ini menghasilkan ringkasan dalam file summarize_update.md.
```
python generate_summary.py
```

d. Menjalankan Chatbot
Eksekusi skrip ini untuk memulai sesi chatbot interaktif.
```
python chatbot.py
```
Untuk menghentikan sesi, ketik exit atau quit.

Demo
https://drive.google.com/file/d/1UoWHN9Vy7gyuI4ACjNCEtrCHbtIcV3MA/view?usp=sharing
