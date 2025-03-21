import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  

st.title("Dashboard Analisis Data Bike Sharing")
st.write("Dashboard ini menyajikan analisis data peminjaman sepeda berdasarkan musim, suhu, dan faktor lainnya.")

@st.cache_data
def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        file_path = os.path.join(project_root, "data", "day.csv")
        st.write(f"Looking for file at: {file_path}")
        
        if not os.path.exists(file_path):
            st.error(f"Data file not found at: {file_path}")
            return None
            
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

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

# Analisis Manual Grouping: Kategori Waktu Pagi, Siang, Sore, Malam
def categorize_time(hour):
    if 6 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 18:
        return 'Siang'
    elif 18 <= hour < 24:
        return 'Sore'
    else:
        return 'Malam'

df['Time_Category'] = df['hr'].apply(categorize_time)

st.subheader("Analisis Manual Grouping Berdasarkan Kategori Waktu")
selected_time_category = st.multiselect("Pilih Kategori Waktu:", ['Pagi', 'Siang', 'Sore', 'Malam'], default=['Pagi', 'Siang', 'Sore', 'Malam'])
filtered_df_time = df[df['Time_Category'].isin(selected_time_category)]

time_grouping = filtered_df_time.groupby('Time_Category')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='Time_Category', y='cnt', data=time_grouping, palette='coolwarm', ax=ax)
plt.xlabel('Kategori Waktu (Pagi, Siang, Sore, Malam)')
plt.ylabel('Total Peminjaman Sepeda')
plt.title('Distribusi Peminjaman Sepeda Berdasarkan Kategori Waktu')
st.pyplot(fig)

st.subheader("Insight")
st.write("1. Peminjaman sepeda tertinggi terjadi pada musim Fall, sedangkan Spring memiliki jumlah penyewaan terendah.")
st.write("2. Terdapat korelasi positif antara suhu dan jumlah peminjaman sepeda, artinya semakin hangat suhu, semakin banyak peminjam.")
st.write("3. Hari kerja cenderung memiliki jumlah peminjam yang lebih tinggi dibandingkan akhir pekan.")
st.write("4. Peminjaman sepeda berdasarkan kategori waktu menunjukkan waktu Siang dan Sore memiliki jumlah peminjam yang signifikan.")