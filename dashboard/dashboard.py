import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dashboard/all_df.csv')

selected_column = st.selectbox("Pilih dataset", ['Semua', 'Jam', 'Hari'])

if selected_column == 'Jam':
    df = df[[col for col in df.columns if col[-4:] == "Hour"]]
elif selected_column == 'Hari':
    df = df[[col for col in df.columns if col[-3:] == "Day"]]
    df = df.drop_duplicates(subset=['instantDay'])
else:
    df = df

st.dataframe(df)