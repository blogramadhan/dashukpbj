import streamlit as st
import pandas as pd

# Fungsi-Fungsi yang bisa digunakan
## Fungsi Baca Dataframe
@st.experimental_memo(ttl=600)
def baca_parquet(dataset):
    return pd.read_parquet(dataset)

## Fungsi Download Dataframe ke CSV
def unduh_data(unduhdata):
    return unduhdata.to_csv(index=False).encode('utf')