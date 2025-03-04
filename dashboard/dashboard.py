import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def penyewa_terbanyak(df):
    data = df.groupby(by="season").agg({
        "mnth": "max",
        "cnt": ["min", "max"]
    }).sort_values(by=("cnt", "max"), ascending=False)

    # Menghapus MultiIndex agar lebih rapi
    data.columns = ["_".join(col).strip() for col in data.columns]
    data.reset_index(inplace=True)

    st.dataframe(data)

def penyewaan_berdasarkan_hari(df):
    st.write("Rata-rata penyewaan pada kondisi cuaca tertentu berdasarkan hari")

    data = df.groupby(['weekday', 'weathersit'])['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='weekday', y='cnt', hue='weathersit', data=data, palette='magma', ax=ax)

    ax.set_title('Rata-Rata Penyewaan Sepeda per Hari berdasarkan Kondisi Cuaca', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
    ax.set_ylabel('Rata-Rata Penyewaan', fontsize=12)
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=10)

    ax.legend(title='Kondisi Cuaca')

    st.pyplot(fig)

def penyewaan_berdasarkan_jam(df):
    st.write("Rata-rata penyewaan pada kondisi cuaca tertentu berdasarkan jam")

    data = df.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()

    pivot_data = data.pivot(index='hr', columns='weathersit', values='cnt')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_data, cmap="magma", annot=True, fmt=".0f", linewidths=0.5, ax=ax)

    ax.set_title('Rata-Rata Penyewaan Sepeda per Jam berdasarkan Kondisi Cuaca', fontsize=14, fontweight='bold')
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Jam dalam Sehari', fontsize=12)
    ax.yaxis.set_tick_params(rotation=0)

    st.pyplot(fig)

def pengaruh_cuaca_terhadap_penyewaan_hari(df):
    st.write("Pengaruh Cuaca terharap Penyewaan berdasarkan Hari")

    data = df.groupby(['mnth', 'weathersit'])['cnt'].mean().reset_index()
    data = data.sort_values(by='mnth')

    palette = list(reversed(sns.color_palette("RdBu", 3)))

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=data, marker='o', palette=palette)

    plt.title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Bulan')
    plt.ylabel('Rata - Rata Penyewaan Sepeda')
    plt.xticks(ticks=range(1, 13), labels=[
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ])
    plt.legend(title="Kondisi Cuaca")
    st.pyplot(plt)

def pengaruh_cuaca_terhadap_penyewaan_jam(df):
    st.write("Pengaruh Cuaca terharap Penyewaan berdasarkan Jam")

    data = df.groupby(['mnth', 'weathersit'])['cnt'].mean().reset_index()
    data = data.sort_values(by='mnth')

    palette = list(reversed(sns.color_palette("RdBu", 4)))

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=data, marker='o', palette=palette)

    plt.title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Bulan')
    plt.ylabel('Rata - Rata Penyewaan Sepeda')
    plt.xticks(ticks=range(1, 13), labels=[
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ])
    plt.legend(title="Kondisi Cuaca")
    st.pyplot(plt)

day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

st.header("Visualisasi Penyewaan Sepeda pada Berbagai Kondisi Cuaca")

col1, col2 = st.columns(2)

with col1:
    st.write('per-hari')
    penyewa_terbanyak(day_df)

with col2:
    st.write('per-jam')
    penyewa_terbanyak(hour_df)

penyewaan_berdasarkan_hari(day_df)
penyewaan_berdasarkan_jam(hour_df)

pengaruh_cuaca_terhadap_penyewaan_hari(day_df)
pengaruh_cuaca_terhadap_penyewaan_jam(hour_df)

