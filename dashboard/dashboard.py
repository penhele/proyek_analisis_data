import streamlit as st
import pandas as pd

df = pd.read_csv('dashboard/all_df.csv')

selected_column = st.selectbox("Pilih dataset", ['Semua', 'Jam', 'Hari'])

if selected_column == 'Jam':
    df = df[['dteday'] + [col for col in df.columns if 'Hour' in col or col == 'hr']]
elif selected_column == 'Hari':
    df = df[['dteday'] + [col for col in df.columns if 'Day' in col and col != 'hr']]
    df = df.drop_duplicates(subset=['instantDay'])
else:
    df = df

st.dataframe(df)