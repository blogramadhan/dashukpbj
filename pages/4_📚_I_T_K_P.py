import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

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

# Konfigurasi variabel lokasi UKPBJ
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

tahuns = [2022, 2023]

pilih = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)
tahun = st.sidebar.selectbox("Pilih Tahun :", tahuns)

if pilih == "KAB. BENGKAYANG":
    kodeFolder = "BKY"
elif pilih == "KAB. KAPUAS HULU":
    kodeFolder = "KPH"
elif pilih == "KAB. KAYONG UTARA":
    kodeFolder = "KKU"
elif pilih == "KAB. KETAPANG":
    kodeFolder = "KTP"
elif pilih == "KAB. KUBU RAYA":
    kodeFolder = "KKR"
elif pilih == "KAB. LANDAK":
    kodeFolder = "LDK"
elif pilih == "KAB. MELAWI":
    kodeFolder = "MLW"
elif pilih == "KAB. MEMPAWAH":
    kodeFolder = "MPW"
elif pilih == "KAB. SAMBAS":
    kodeFolder = "SBS"
elif pilih == "KAB. SANGGAU":
    kodeFolder = "SGU"
elif pilih == "KAB. SEKADAU":
    kodeFolder = "SKD"
elif pilih == "KAB. SINTANG":
    kodeFolder = "STG"
elif pilih == "KOTA PONTIANAK":
    kodeFolder = "PTK"
elif pilih == "KOTA SINGKAWANG":
    kodeFolder = "SKW"
elif pilih == "PROV. KALBAR":
    kodeFolder = "PROV"


# Buat tab ITKP UKPBJ dan ITKP Perangkat Daerah
tab1, tab2 = st.tabs(["ITKP UKPBJ", "ITKP PD"])

# Tab ITKP UKPBJ
with tab1:

    ## Dataset ITKP UKPBJ
    DatasetSIRUPDP = f"data/ITKP/{kodeFolder}/sirupdp{str(tahun)}.parquet"
    DatasetSIRUPSW = f"data/ITKP/{kodeFolder}/sirupsw{str(tahun)}.parquet"
    DatasetSIRUPDSARSAP = f"data/ITKP/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
    DatasetTENDERDTS = f"data/ITKP/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
    DatasetTENDERDTKS = f"data/ITKP/{kodeFolder}/dtender_dtks{str(tahun)}.parquet"
    DatasetNTENDERDNTS = f"data/ITKP/{kodeFolder}/dntender_dnts{str(tahun)}.parquet"
    DatasetKATALOG = f""

    ### Data RUP paket penyedia

    ### Data RUP paket swakelola

    ### Data struktur anggaran RUP
    df_rsap = pd.read_parquet(DatasetSIRUPDSARSAP)

    ### Data Tender

    ### Data Non Tender

    ### Data Katalog

    ## Mulai tampilkan data ITKP UKPBJ
    #st.subheader(f"DATA ITKP TAHUN {tahun} - {pilih}")

    ## Tampilan pemanfaatan SIRUP
    st.markdown(f"## **PEMANFAATAN SIRUP - {tahun}**")
    ### RUP struktur anggaran
    st.markdown(f"### Struktur Anggaran")
    belanja_pengadaan = df_rsap['belanja_pengadaan'].sum()
    belanja_pengadaan_print = format_currency(belanja_pengadaan, 'Rp. ', locale='id_ID')
    belanja_operasional = df_rsap['belanja_operasi'].sum()
    belanja_operasional_print = format_currency(belanja_operasional, 'Rp. ', locale='id_ID')
    belanja_modal = df_rsap['belanja_modal'].sum()
    belanja_modal_print = format_currency(belanja_modal, 'Rp. ', locale='id_ID')

    sa1, sa2, sa3 = st.columns(3)
    sa1.metric("Belanja Pengadaan", belanja_pengadaan_print)
    sa2.metric("Belanja Operasional", belanja_operasional_print)
    sa3.metric("Belanja Modal", belanja_modal_print)

# Tab ITKP PD
with tab2:

    ## Dataset ITKP PD

    ## Mulai tampilkan data ITKP Perangkat Daerah
    st.subheader(f"DATA ITKP TAHUN {tahun} - PERANGKAT DAERAH")