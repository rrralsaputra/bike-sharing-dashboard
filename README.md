# 🚲 Bike Sharing Data Analytics Dashboard
Proyek ini mencakup proses pembersihan data (*data wrangling*), eksplorasi data (*exploratory data analysis* / EDA), penerapan teknik analisis lanjutan (*clustering/binning*), hingga pembuatan *dashboard* interaktif menggunakan Streamlit.

## Struktur Direktori
- `dashboard/` : Berisi file Python utama untuk menjalankan aplikasi Streamlit (`dashboard.py`) beserta file dataset pendukungnya.
- `data/` : Berisi file dataset mentah asli (`day.csv` dan `hour.csv`).
- `notebook.ipynb` : File Jupyter Notebook yang memuat dokumentasi lengkap seluruh alur proses analisis data dari awal hingga penarikan kesimpulan.
- `README.md` : Dokumentasi petunjuk penggunaan (file yang sedang kamu baca ini).
- `requirements.txt` : Daftar *library* Python yang dibutuhkan untuk menjalankan *dashboard*.
- `url.txt` : Tautan untuk mengakses *dashboard* yang sudah di-*deploy* secara publik.

## Cara Menjalankan Dashboard di Local
Untuk menjalankan *dashboard* ini di komputer kamu sendiri, silakan ikuti langkah-langkah berikut:

### 1. Persiapan Lingkungan (Environment)
Pastikan Python sudah terinstal. Buka Terminal atau Command Prompt, lalu arahkan direktori ke folder proyek ini. (Penggunaan *virtual environment* sangat disarankan).

```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment (Windows)
venv\Scripts\activate

# Mengaktifkan virtual environment (Mac/Linux)
source venv/bin/activate
```
### 2. Instalasi Dependensi
Instal semua library yang dibutuhkan dengan menjalankan perintah ini:
```
pip install -r requirements.txt
```
### 3. Menjalankan Aplikasi
```
streamlit run dashboard/dashboard.py
