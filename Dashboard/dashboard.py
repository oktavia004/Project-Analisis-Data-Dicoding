import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tampilan visualisasi
sns.set(style="whitegrid")

# Fungsi untuk membaca dan membersihkan data
@st.cache_data
def load_data():
    days_df = pd.read_csv("Dashboard/day.csv")
    hours_df = pd.read_csv("Dashboard/hour.csv")
    
    # Cleaning days_df
    days_df.dropna(inplace=True)
    days_df.drop_duplicates(inplace=True)
    days_df['dteday'] = pd.to_datetime(days_df['dteday'])
    
    # Cleaning hours_df
    hours_df.dropna(inplace=True)
    hours_df.drop_duplicates(inplace=True)
    hours_df['dteday'] = pd.to_datetime(hours_df['dteday'])
    
    return days_df, hours_df

# Memuat data
days_df, hours_df = load_data()

# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda")

# Menampilkan data sampel
if st.checkbox("Tampilkan Data Sampel Hari"):
    st.write(days_df.sample(5))

# Menampilkan visualisasi suhu
st.header("Pengaruh Suhu terhadap Rata-rata Penyewaan Sepeda")
bins = np.linspace(days_df['temp'].min(), days_df['temp'].max(), 10)  
labels = [f'{round(b, 2)} - {round(bins[i+1], 2)}' for i, b in enumerate(bins[:-1])]  
days_df['temp_bins'] = pd.cut(days_df['temp'], bins=bins, labels=labels, include_lowest=True)

temp_rentals_avg = days_df.groupby('temp_bins')['cnt'].mean()

# Visualisasi
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=temp_rentals_avg.index, y=temp_rentals_avg.values, color="skyblue", ax=ax)
plt.xticks(rotation=45) 
plt.title('Pengaruh Suhu terhadap Rata-rata Penyewaan Sepeda')
plt.xlabel('Rentang Suhu')
plt.ylabel('Rata-rata Penyewaan Sepeda')

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan pola musiman
st.header("Pola Musiman dalam Penyewaan Sepeda")
season_avg_rentals = days_df.groupby('season')['cnt'].mean().reset_index()
season_labels = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
season_avg_rentals['season'] = season_avg_rentals['season'].map(season_labels)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_avg_rentals, color="skyblue", ax=ax2)
plt.title('Pola Musiman dalam Penyewaan Sepeda')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan Sepeda')

# Menampilkan plot di Streamlit
st.pyplot(fig2)

# Menampilkan heatmap
st.header("Rata-rata Penyewaan Sepeda Berdasarkan Bulan dan Musim")
seasonal_heatmap = days_df.pivot_table(index='season', columns='mnth', values='cnt', aggfunc='mean')
season_labels = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
seasonal_heatmap.index = seasonal_heatmap.index.map(season_labels)

fig3, ax3 = plt.subplots(figsize=(12, 8))
sns.heatmap(seasonal_heatmap, cmap='YlGnBu', annot=True, fmt='.1f', linewidths=.5, ax=ax3, cbar_kws={"label": "Rata-rata Penyewaan Sepeda"})
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Bulan dan Musim', fontsize=16)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Musim', fontsize=12)
plt.xticks(ticks=np.arange(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.yticks(rotation=0)

# Menampilkan plot di Streamlit
st.pyplot(fig3)
