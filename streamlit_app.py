import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_penyewa_bulanan_df(df):
    penyewa_bulanan_df = df.groupby(['yr','mnth'])['cnt'].sum().reset_index()
    return penyewa_bulanan_df

def create_rata_rata_penyewa_df(df):
    penyewa_bulanan_df = create_penyewa_bulanan_df(df)
    hari_dalam_bulan = df.groupby(['yr','mnth'])['cnt'].count().reset_index()
    rata_rata_penyewa_df = penyewa_bulanan_df.merge(hari_dalam_bulan, on=['yr','mnth'], suffixes=('_total', '_count'))
    rata_rata_penyewa_df['cnt_avg'] = rata_rata_penyewa_df['cnt_total'] / rata_rata_penyewa_df['cnt_count']
    ganti_bulan = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    ganti_tahun={0: 2011, 1: 2012}
    rata_rata_penyewa_df['mnth'] = penyewa_bulanan_df['mnth'].map(ganti_bulan)
    rata_rata_penyewa_df['yr'] = rata_rata_penyewa_df['yr'].map(ganti_tahun)
    return rata_rata_penyewa_df[['yr', 'mnth', 'cnt_avg']]

def ganti_musim(df):
    ganti_value_season = {1:'spring', 2:'summer', 3:'fall', 4:'winter'}
    df['season']= cek_sewa_musim_harian['season'].map(ganti_value_season)
    return df

df=pd.read_csv('day.csv')
rata_rata_bulan=create_rata_rata_penyewa_df(df)
rata_rata_bulan['tahun_bulan'] = rata_rata_bulan['mnth'] + " " + rata_rata_bulan['yr'].astype(str)
cek_sewa_musim_harian=df.groupby('season')['cnt'].sum().reset_index()
cek_sewa_musim_harian=ganti_musim(cek_sewa_musim_harian)
mean_kerja = df[df['workingday'] == 1]['cnt'].mean()
mean_libur = df[df['workingday'] == 0]['cnt'].mean()
mean_total = pd.DataFrame({
    'workingday':['Kerja', 'Libur'], 
    'sewa':[mean_kerja, mean_libur]
})


st.title("Data Penyewaan Sepeda")
st.header(
    "Melihat persebaran data penyewaan sepeda."
)
col1, col2 = st.columns(2)
with col1:
    st.metric("Total penyewa sepeda dalam dua tahun: ", cek_sewa_musim_harian['cnt'].sum())
    st.metric("Rata-rata penyewa sepeda tiap hari: ", int(mean_total['sewa'].mean()))
with col2:
    st.metric("Total penyewa terdaftar dalam dua tahun: ", df['registered'].sum())
    st.metric("Total penyewa kasual dalam dua tahun: ", df['casual'].sum())
st.header("Grafik tiap bulan")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt_avg", 
    x="tahun_bulan",
    data=rata_rata_bulan,
    palette="viridis", 
    ax=ax
)

ax.set_xticklabels(rata_rata_bulan['tahun_bulan'], rotation=90, ha='center')
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.header("Grafik berdasarkan musim")
col1, col2 = st.columns([1,1])
with col1:
    st.subheader("Grafik total sepeda tersewakan")
    fig1, ax1 = plt.subplots(figsize=(20, 15))
    sns.barplot(
        y="cnt", 
        x="season",
        data=cek_sewa_musim_harian,
        palette="viridis", 
        ax=ax1
    )
    ax1.set_xticklabels(cek_sewa_musim_harian['season'], ha='center')
    ax1.set_ylabel(None)
    ax1.set_xlabel(None)
    ax1.tick_params(axis='x', labelsize=35)
    ax1.tick_params(axis='y', labelsize=30)
    st.pyplot(fig1)
with col2:
    st.subheader("Distribusi sewa sepeda tiap musim")
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(cek_sewa_musim_harian['cnt'], labels=cek_sewa_musim_harian['season'],
        autopct='%1.1f%%', shadow=False, startangle=100, textprops={'fontsize': 30})

    ax2.axis('equal')
    st.pyplot(fig2)

st.header("Grafik berdasarkan hari libur atau kerja")
st.text("")
col1, col2 = st.columns([1,1])
with col1:
    st.subheader("Grafik total sepeda tersewakan")
    fig1, ax1 = plt.subplots(figsize=(20, 20))
    sns.barplot(
        y="sewa", 
        x="workingday",
        data=mean_total,
        palette="viridis", 
        ax=ax1
    )
    ax1.set_xticklabels(cek_sewa_musim_harian['season'], ha='center')
    ax1.set_ylabel(None)
    ax1.set_xlabel(None)
    ax1.tick_params(axis='x', labelsize=35)
    ax1.tick_params(axis='y', labelsize=30)
    st.pyplot(fig1)
with col2:
    st.subheader("Distribusi sewa sepeda tiap musim")
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(mean_total['sewa'], labels=mean_total['workingday'],
        autopct='%1.1f%%', shadow=False, startangle=100, textprops={'fontsize': 30})

    ax2.axis('equal')
    st.pyplot(fig2)
