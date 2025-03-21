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
        # Get the current script's directory
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

min_temp, max_temp = st.slider("Pilih Rentang Suhu:", float(df['temp'].min()), float(df['temp'].max()), (float(df['temp'].min()), float(df['temp'].max())))
filtered_df_temp = df[(df['temp'] >= min_temp) & (df['temp'] <= max_temp)]

st.subheader("Hubungan antara Suhu dan Jumlah Peminjam")
fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x='temp', y='cnt', data=filtered_df_temp, alpha=0.6)
plt.xlabel('Suhu Udara (Normalized)')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.title('Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda')
st.pyplot(fig)

max_rental_temp = df.loc[df['cnt'].idxmax(), 'temp']
st.write(f"Jumlah peminjaman sepeda mencapai puncaknya pada suhu: {max_rental_temp}")

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

# Pengelompokan Manual: Berdasarkan Jumlah Peminjaman Sepeda
def group_rental_usage(cnt):
    if cnt < 2000:
        return 'Low Usage'
    elif 2000 <= cnt < 4000:
        return 'Medium Usage'
    else:
        return 'High Usage'

df['rental_group'] = df['cnt'].apply(group_rental_usage)

st.subheader("Distribusi Penggunaan Sepeda (Manual Grouping)")
selected_rental_groups = st.multiselect("Pilih Kelompok Penggunaan:", ['Low Usage', 'Medium Usage', 'High Usage'], default=['Low Usage', 'Medium Usage', 'High Usage'])
filtered_df_rental = df[df['rental_group'].isin(selected_rental_groups)]
rental_group_counts = filtered_df_rental['rental_group'].value_counts().reset_index()
rental_group_counts.columns = ['Group', 'Count']

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='Group', y='Count', data=rental_group_counts, palette='pastel', ax=ax)
plt.xlabel('Kelompok Penggunaan')
plt.ylabel('Jumlah Hari')
plt.title('Distribusi Penggunaan Sepeda Berdasarkan Kelompok')
st.pyplot(fig)

# Pengelompokan Manual: Berdasarkan Suhu
def group_temperature(temp):
    if temp < 0.3:
        return 'Cool'
    elif 0.3 <= temp < 0.6:
        return 'Moderate'
    else:
        return 'Hot'

df['temperature_group'] = df['temp'].apply(group_temperature)

st.subheader("Distribusi Berdasarkan Suhu")
selected_temp_groups = st.multiselect("Pilih Kelompok Suhu:", ['Cool', 'Moderate', 'Hot'], default=['Cool', 'Moderate', 'Hot'])
filtered_df_temp_group = df[df['temperature_group'].isin(selected_temp_groups)]
temp_group_counts = filtered_df_temp_group['temperature_group'].value_counts().reset_index()
temp_group_counts.columns = ['Temperature Group', 'Count']

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='Temperature Group', y='Count', data=temp_group_counts, palette='cool', ax=ax)
plt.xlabel('Kelompok Suhu')
plt.ylabel('Jumlah Hari')
plt.title('Distribusi Hari Berdasarkan Suhu Udara')
st.pyplot(fig)

st.subheader("Insight Tambahan")
st.write("1. Mayoritas hari berada dalam kategori **Moderate** suhu, yang menunjukkan bahwa suhu sedang lebih mendominasi.")
st.write("2. Penggunaan sepeda didominasi oleh kelompok **Medium Usage**, yang berarti peminjaman sepeda tidak terlalu ekstrem.")

st.subheader("Insight")
st.write("1. Peminjaman sepeda tertinggi terjadi pada musim Fall, sedangkan Spring memiliki jumlah penyewaan terendah.")
st.write("2. Terdapat korelasi positif antara suhu dan jumlah peminjaman sepeda, artinya semakin hangat suhu, semakin banyak peminjam.")
st.write("3. Hari kerja cenderung memiliki jumlah peminjam yang lebih tinggi dibandingkan akhir pekan.")
