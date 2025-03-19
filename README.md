
# 🚴‍♂️ Dashboard Analisis Data Bike Sharing

## 📌 Deskripsi
Dashboard interaktif ini dibuat menggunakan **Streamlit** untuk menganalisis data peminjaman sepeda berdasarkan musim dan suhu. Dashboard ini memungkinkan pengguna untuk melihat tren penggunaan sepeda serta hubungan antara variabel-variabel penting dalam dataset.

---

## 🚀 Cara Menjalankan Dashboard

### 1️⃣ **Persiapan**
Pastikan Python sudah terinstal di sistem Anda. Jika belum, unduh dan instal dari [python.org](https://www.python.org/). Setelah itu, pastikan Anda telah menginstal pustaka yang diperlukan dengan perintah berikut:

```sh
pip install -r requirements.txt
```

### 2️⃣ **Menjalankan Aplikasi**
1. **Buka Terminal / Command Prompt**
2. **Navigasikan ke direktori proyek**
   ```sh
   cd "C:/Users/johan/OneDrive/Documents/#Materi/1Dicoding"
   ```
3. **Jalankan Streamlit**
   ```sh
   streamlit run dashboard.py
   ```
4. **Buka browser** dan akses **http://localhost:8501**

---

## 📂 Struktur Proyek
```
📂 Bike-Sharing-Analysis
│── 📄 dashboard.py                
│── 📄 requirements.txt      
│── 📄 README.md              
│── 📂 data/                  
│   ├── day.csv
│   ├── hour.csv
│   ├── Merge_Bike_Sharing_data.csv
```

---

## 🔧 Troubleshooting
✅ **ModuleNotFoundError** → Jalankan `pip install -r requirements.txt` untuk menginstal semua dependensi.
✅ **Dataset Tidak Ditemukan** → Pastikan file **day.csv** dan **hour.csv** ada di folder **data/**.
✅ **Streamlit Tidak Berjalan** → Pastikan Anda menjalankan perintah `streamlit run dashboard.py` di direktori proyek yang benar.

---

## 📞 Kontak
Jika ada pertanyaan atau masalah, silakan hubungi **Johan Adrian** melalui email: **johantgg113@gmail.com**.



