import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('📊 Analisis Bike Sharing Dataset')

df = pd.read_csv('dashboard/all_df.csv')

def home_page(df):
    st.write('Dataset berikut telah dibersihkan dan siap digunakan untuk visualisasi Bike Sharing. Anda dapat memilih untuk melihat data dalam format per jam atau per hari sesuai kebutuhan.')

    selected_column = st.selectbox("Pilih menu", ['Semua', 'Jam', 'Hari'])

    if selected_column == 'Jam':
        df = df[['dteday'] + [col for col in df.columns if 'Hour' in col or col == 'hr']]
    elif selected_column == 'Hari':
        df = df[['dteday'] + [col for col in df.columns if 'Day' in col and col != 'hr']]
        df = df.drop_duplicates(subset=['instantDay'])

    st.dataframe(df)

    st.write('Menu jam merupakan rincian dari menu hari, yang memberikan detail tentang kejadian setiap harinya. Seperti yang kita ketahui, satu hari terdiri dari 24 jam. Oleh karena itu, pada kolom "hr" (menu jam), waktu dimulai dari 0 hingga 23.')  

def analysis_page(df):
    def visualize_seasonal_impact(df):
        df["dteday"] = pd.to_datetime(df["dteday"]) 
        df["year"] = df["dteday"].dt.year

        selected_years = st.multiselect("Pilih Tahun:", [2011, 2012], default=[2011, 2012], key="bike_year_selector")

        if not selected_years:
            st.warning("Pilih setidaknya satu tahun untuk ditampilkan.")
            return

        df_filtered = df[df["year"].isin(selected_years)]

        season_df = df_filtered.groupby(["year", "seasonDay"]).agg({
            "cntDay": ["mean", "sum", "count"]
        }).sort_values(by=("cntDay", "mean"), ascending=False).reset_index()

        fig, axes = plt.subplots(1, len(selected_years), figsize=(15, 6), sharey=True)

        if len(selected_years) == 1:
            axes = [axes]

        for i, year in enumerate(selected_years):
            sns.barplot(
                ax=axes[i], data=season_df[season_df["year"] == year], 
                x="seasonDay", y=("cntDay", "mean"), hue="seasonDay", 
                palette="coolwarm", legend=False
            )
            axes[i].set_title(f"Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda ({year})", fontsize=14)
            axes[i].set_xlabel("Kondisi Cuaca")
            if i == 0:
                axes[i].set_ylabel("Total Penyewaan Sepeda")
            else:
                axes[i].set_ylabel("")

        plt.tight_layout()

        st.pyplot(fig)

    def bike_rental_by_month(df):
        df["dteday"] = pd.to_datetime(df["dteday"])
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        df["month"] = df["dteday"].dt.strftime('%b') 
        df["month_num"] = df["dteday"].dt.month
        df["year"] = df["dteday"].dt.year
        
        selected_years = st.multiselect("Pilih Tahun:", [2011, 2012], default=[2011, 2012], key="season_year_selector")

        if not selected_years:
            st.warning("Pilih setidaknya satu tahun untuk ditampilkan.")
            return

        selected_month_range = st.slider("Pilih Rentang Bulan:", 
                                        min_value=1, max_value=12, 
                                        value=(1, 12), 
                                        format="%d") 

        start_month, end_month = selected_month_range
        selected_months = month_order[start_month - 1:end_month]

        df_filtered = df[(df["year"].isin(selected_years)) & (df["month"].isin(selected_months))]

        def get_monthly_rentals(df):
            return df.groupby(["year", "month"]).agg({"cntDay": "mean"}).unstack(level=0).reindex(month_order)

        monthly_rentals = get_monthly_rentals(df_filtered)
        
        fig, ax = plt.subplots(figsize=(10, 5))

        for year in selected_years:
            if year in monthly_rentals.columns.get_level_values(1):
                ax.plot(monthly_rentals.index, monthly_rentals["cntDay", year], marker='o', linewidth=2, label=f"{year}")

        ax.set_title("Jumlah Penyewaan Sepeda per Bulan", fontsize=14)
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Penyewaan")
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title="Tahun")
        
        plt.tight_layout()
        
        st.pyplot(fig)

    st.subheader('Apakah musim dingin mengurangi jumlah penyewaan sepeda?')
    visualize_seasonal_impact(df)

    st.divider()

    st.subheader('Pada bulan apa penyewaan sepeda paling banyak terjadi?')
    bike_rental_by_month(df)

    st.divider()

    st.subheader('Conclusion')
    st.markdown("""
        - Musim dingin mengurangi jumlah penyewaan sepeda. Dapat dilihat bersama bahwa pada tahun 2011 dan 2012, jumlah penyewaan sepeda musim dingin selalu paling sedikit.
        - Pada tahun 2011, bulan Juni rata-rata paling banyak penyewaan. Sedangkan pada tahun 2012, bulan September rata-rata paling banyak penyewaan.
    """)


if "page" not in st.session_state:
    st.session_state["page"] = "home"

with st.sidebar:
    if st.button('Halaman Utama'):
        st.session_state['page'] = 'home'
    if st.button('Analisis Data'):
        st.session_state['page'] = 'analysis'

if st.session_state['page'] == "home":
    home_page(df)

elif st.session_state['page'] == "analysis":
    analysis_page(df)
