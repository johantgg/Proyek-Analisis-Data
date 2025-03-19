import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  

st.title("Dashboard Analisis Data Bike Sharing")
st.write("Dashboard ini menyajikan analisis data peminjaman sepeda berdasarkan musim, suhu, dan faktor lainnya.")

@st.cache_data
def load_data():
    file_path = os.path.join("Data", "day.csv")  
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.subheader("Tampilkan Data")
st.write(df.head())

# Fitur interaktif: Filter berdasarkan Musim
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_options)

st.subheader("Pilih Musim")
selected_seasons = []

# Checkbox untuk memilih musim
all_seasons = st.checkbox("All Seasons", value=True)
spring = st.checkbox("Spring", value=True)
summer = st.checkbox("Summer", value=True)
fall = st.checkbox("Fall", value=True)
winter = st.checkbox("Winter", value=True)

if all_seasons:
    selected_seasons = list(season_options.values())
else:
    if spring:
        selected_seasons.append("Spring")
    if summer:
        selected_seasons.append("Summer")
    if fall:
        selected_seasons.append("Fall")
    if winter:
        selected_seasons.append("Winter")

if not selected_seasons:
    st.warning("Pilih setidaknya satu musim untuk ditampilkan.")
    selected_seasons = df['season_label'].unique()

filtered_df = df[df['season_label'].isin(selected_seasons)]

fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(x='season_label', y='cnt', data=filtered_df, palette='viridis', ax=ax)
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
st.pyplot(fig)

# Fitur interaktif: Filter berdasarkan Rentang Suhu
min_temp, max_temp = st.slider("Pilih Rentang Suhu:", float(df['temp'].min()), float(df['temp'].max()), (float(df['temp'].min()), float(df['temp'].max())))
filtered_df_temp = df[(df['temp'] >= min_temp) & (df['temp'] <= max_temp)]

st.subheader("Hubungan antara Suhu dan Jumlah Peminjam")
fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x='temp', y='cnt', data=filtered_df_temp, alpha=0.6)
plt.xlabel('Suhu Udara (Normalized)')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.title('Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda')
st.pyplot(fig)

# Menentukan suhu saat jumlah peminjaman sepeda mencapai puncaknya
max_rental_temp = df.loc[df['cnt'].idxmax(), 'temp']
st.write(f"Jumlah peminjaman sepeda mencapai puncaknya pada suhu: {max_rental_temp}")

# Analisis RFM
st.subheader("Analisis RFM untuk Peminjaman Sepeda")
df['date'] = pd.to_datetime(df['dteday'])
latest_date = df['date'].max()
rfm_df = df.groupby('instant').agg({
    'date': lambda x: (latest_date - x.max()).days,
    'instant': 'count',
    'cnt': 'sum'
}).rename(columns={'date': 'Recency', 'instant': 'Frequency', 'cnt': 'Monetary'})

st.write("Hasil Analisis RFM:")
st.write(rfm_df.head())

# Fitur interaktif untuk memilih jenis distribusi RFM
rfm_metric = st.selectbox("Pilih Metode Distribusi RFM:", ['Recency', 'Frequency', 'Monetary'])
fig, ax = plt.subplots(figsize=(8,5))
sns.histplot(rfm_df[rfm_metric], bins=20, kde=True, ax=ax)
plt.xlabel(rfm_metric)
plt.ylabel('Frekuensi')
plt.title(f'Distribusi {rfm_metric} Peminjaman Sepeda')
st.pyplot(fig)

# Fitur interaktif: Rata-rata Penyewaan Sepeda per Hari dalam Seminggu
day_labels = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
df['weekday_label'] = df['weekday'].map(day_labels)

day_avg = df.groupby('weekday_label')['cnt'].mean().reset_index()
st.subheader("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu")
selected_days = st.multiselect("Pilih Hari:", day_labels.values(), default=list(day_labels.values()))
filtered_day_avg = day_avg[day_avg['weekday_label'].isin(selected_days)]

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x='weekday_label', y='cnt', data=filtered_day_avg, palette='coolwarm', ax=ax)
plt.xlabel('Hari')
plt.ylabel('Rata-rata Penyewaan')
plt.title('Rata-rata Penyewaan Sepeda per Hari dalam Seminggu')
st.pyplot(fig)

st.subheader("Insight")
st.write("1. Peminjaman sepeda tertinggi terjadi pada musim Fall, sedangkan Spring memiliki jumlah penyewaan terendah.")
st.write("2. Terdapat korelasi positif antara suhu dan jumlah peminjaman sepeda, artinya semakin hangat suhu, semakin banyak peminjam.")
st.write("3. Hari kerja cenderung memiliki jumlah peminjam yang lebih tinggi dibandingkan akhir pekan.")
st.write("4. Analisis RFM menunjukkan sebaran pengguna berdasarkan seberapa sering dan baru mereka menyewa sepeda.")
