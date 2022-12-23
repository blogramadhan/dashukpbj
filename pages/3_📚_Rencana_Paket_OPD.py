#####################################################################################
# Source code: Dashboard analisa data Pengadaan Barang dan Jasa di Kalimantan Barat #
#-----------------------------------------------------------------------------------#
# Dashboard ini dibuat oleh:                                                        #
# Nama          : Kurnia Ramadhan, ST.,M.Eng                                        #
# Jabatan       : Sub Koordinator Pengelolaan Informasi LPSE                        #
# Instansi      : Biro Pengadaan Barang dan Jasa Setda Prov. Kalbar                 #
# Email         : kramadhan@gmail.com                                               #
# URL Web       : https://github.com/blogramadhan                                   #
#-----------------------------------------------------------------------------------#
# Hak cipta milik Allah SWT, source code ini silahkan dicopy, di download atau      #
# di distribusikan ke siapa saja untuk bahan belajar, atau untuk dikembangkan lagi  #
# lebih lanjut, btw tidak untuk dijual ya.                                          #
#                                                                                   #
# Jika teman-teman mengembangkan lebih lanjut source code ini, agar berkenan untuk  #
# men-share code yang teman-teman kembangkan lebih lanjut sebagai bahan belajar     #
# untuk kita semua.                                                                 #
#-----------------------------------------------------------------------------------#
# @ Pontianak, 2022                                                                 #
#####################################################################################

# Import library
import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from fungsi import *

# Setting CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hilangkan menu Streamlit di sudut kanan atas
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Konfigurasi variabel lokasi UPBJ
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

tahuns = [2022, 2023]

pilih = st.sidebar.selectbox("Pilih UPBJ yang diinginkan :", daerah)
tahun = st.sidebar.selectbox("Pilih Tahun :", tahuns)

if pilih == "KAB. BENGKAYANG":
    kodeFolder = "bky"
elif pilih == "KAB. KAPUAS HULU":
    kodeFolder = "kph"
elif pilih == "KAB. KAYONG UTARA":
    kodeFolder = "kku"
elif pilih == "KAB. KETAPANG":
    kodeFolder = "ktp"
elif pilih == "KAB. KUBU RAYA":
    kodeFolder = "kkr"
elif pilih == "KAB. LANDAK":
    kodeFolder = "ldk"
elif pilih == "KAB. MELAWI":
    kodeFolder = "mlw"
elif pilih == "KAB. MEMPAWAH":
    kodeFolder = "mpw"
elif pilih == "KAB. SAMBAS":
    kodeFolder = "sbs"
elif pilih == "KAB. SANGGAU":
    kodeFolder = "sgu"
elif pilih == "KAB. SEKADAU":
    kodeFolder = "skd"
elif pilih == "KAB. SINTANG":
    kodeFolder = "stg"
elif pilih == "KOTA PONTIANAK":
    kodeFolder = "ptk"
elif pilih == "KOTA SINGKAWANG":
    kodeFolder = "skw"
elif pilih == "PROV. KALBAR":
    kodeFolder = "prov"