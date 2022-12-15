import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Hilangkan menu Streamlit di sudut kanan atas
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Konfigurasi variabel lokasi UKPBJ
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

tahuns = [2022, 2023]

pilih = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)
tahun = st.sidebar.selectbox("Pilih Tahun :", tahuns)

if pilih == "KAB. BENGKAYANG":
    kodeRUP = "D206"
elif pilih == "KAB. KAPUAS HULU":
    kodeRUP = "D209"
elif pilih == "KAB. KAYONG UTARA":
    kodeRUP = "D207"
elif pilih == "KAB. KETAPANG":
    kodeRUP = "D201"
elif pilih == "KAB. KUBU RAYA":
    kodeRUP = "D202"
elif pilih == "KAB. LANDAK":
    kodeRUP = "D205"
elif pilih == "KAB. MELAWI":
    kodeRUP = "D210"
elif pilih == "KAB. MEMPAWAH":
    kodeRUP = "D552"
elif pilih == "KAB. SAMBAS":
    kodeRUP = "D208"
elif pilih == "KAB. SANGGAU":
    kodeRUP = "D204"
elif pilih == "KAB. SEKADAU":
    kodeRUP = "D198"
elif pilih == "KAB. SINTANG":
    kodeRUP = "D211"
elif pilih == "KOTA PONTIANAK":
    kodeRUP = "D199"
elif pilih == "KOTA SINGKAWANG":
    kodeRUP = "D200"
elif pilih == "PROV. KALBAR":
    kodeRUP = "D197"    