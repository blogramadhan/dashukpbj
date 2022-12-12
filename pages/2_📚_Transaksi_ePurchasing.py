import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Setting CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

# Konfigurasi Variabel Lokasi
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

pilih = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)

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

# Fungsi-fungsi buatan
def convert_trxkatalog(dftrx):
    return dftrx.to_csv().encode('utf')

def convert_prodkatalog(dfprod):
    return dfprod.to_csv().encode('utf')

def convert_trxdaring(dftrxdaring):
    return dftrxdaring.to_csv().encode('utf')

# Dataset
DatasetKatalog = "data/epurchasing/katalogdetail.parquet"
DatasetProdukKatalog = "data/epurchasing/prodkatalog.parquet"
DatasetTokoDaring = "data/epurchasing/daring.parquet"

## Data E-KATALOG
#df_kat = pd.read_excel(DatasetKatalog, engine='openpyxl')
#df_prod = pd.read_excel(DatasetProdukKatalog, engine='openpyxl')
df_kat = pd.read_parquet(DatasetKatalog)
df_prod = pd.read_parquet(DatasetProdukKatalog)

df_kat_loc = df_kat[df_kat['kd_klpd'] == kodeRUP]
df_kat_loc_lokal = df_kat_loc[df_kat_loc['jenis_katalog'] == "Lokal"]
df_kat_loc_sektoral = df_kat_loc[df_kat_loc['jenis_katalog'] == "Sektoral"]
df_kat_loc_nasional = df_kat_loc[df_kat_loc['jenis_katalog'] == "Nasional"]
df_prod_loc = df_prod[df_prod['kd_klpd'] == kodeRUP]

## Data Toko Daring
#df_daring = pd.read_excel(DatasetTokoDaring, engine='openpyxl')
df_daring = pd.read_parquet(DatasetTokoDaring)
df_daring_loc = df_daring[df_daring['kd_klpd'] == kodeRUP]

# Buat Tab e-Katalog dan Toko Daring
tab1, tab2 = st.tabs(["E-KATALOG", "TOKO DARING"])

## Tab e-Katalog
with tab1:

    ## Mulai Tampilkan Data E-KATALOG
    st.subheader("TRANSAKSI E-KATALOG - " + pilih)
    jumlah_produk = df_prod_loc['nama_produk'].count()
    jumlah_penyedia = df_prod_loc['nama_penyedia'].value_counts().shape

    jumlah_trx_lokal = df_kat_loc_lokal['no_paket'].value_counts().shape
    nilai_trx_lokal = df_kat_loc_lokal['total_harga'].sum()
    nilai_trx_lokal_print = format_currency(nilai_trx_lokal, 'Rp. ', locale='id_ID')

    jumlah_trx_sektoral = df_kat_loc_sektoral['no_paket'].value_counts().shape
    nilai_trx_sektoral = df_kat_loc_sektoral['total_harga'].sum()
    nilai_trx_sektoral_print = format_currency(nilai_trx_sektoral, 'Rp. ', locale='id_ID')

    jumlah_trx_nasional = df_kat_loc_nasional['no_paket'].value_counts().shape
    nilai_trx_nasional = df_kat_loc_nasional['total_harga'].sum()
    nilai_trx_nasional_print = format_currency(nilai_trx_nasional, 'Rp. ', locale='id_ID')

    dkl1, dkl2, dkl3, dkl4 = st.columns(4)
    dkl1.metric("Jumlah Produk Katalog Lokal", jumlah_produk)
    dkl2.metric("Jumlah Penyedia Katalog Lokal", jumlah_penyedia[0])
    dkl3.metric("Jumlah Transaksi Katalog Lokal", jumlah_trx_lokal[0])
    dkl4.metric("Nilai Transaksi Katalog Lokal", nilai_trx_lokal_print)

    dks1, dks2, dks3 = st.columns(3)
    dks1.metric("Jumlah Produk E-Katalog Sektoral", "Tidak Ada Data")
    dks2.metric("Jumlah Transaksi E-Katalog Sektoral", jumlah_trx_sektoral[0])
    dks3.metric("Nilai Transaksi E-Ketalog Sektoral", nilai_trx_sektoral_print)

    dkn1, dkn2, dkn3 = st.columns(3)
    dkn1.metric("Jumlah Produk E-Katalog Nasional", "Tidak Ada Data")
    dkn2.metric("Jumlah Transaksi E-Katalog Nasional", jumlah_trx_nasional[0])
    dkn3.metric("Nilai Transaksi E-Ketalog Nasional", nilai_trx_nasional_print)

    # Buat grafik Data E-Katalog   
    #opdtrxcount = df_kat_loc_lokal.nama_satker.value_counts().sort_values(ascending=False)
    tmp_kat_loc_lokal = df_kat_loc_lokal[['nama_satker', 'no_paket']]
    pv_kat_loc_lokal = tmp_kat_loc_lokal.pivot_table(
        index = ['nama_satker', 'no_paket'],
        #values = ['no_paket']
    )
    tmp_kat_loc_lokal_ok = pv_kat_loc_lokal.reset_index()
    opdtrxcount = tmp_kat_loc_lokal_ok['nama_satker'].value_counts()
    opdtrxsum = df_kat_loc_lokal.groupby(by='nama_satker').sum().sort_values(by='total_harga', ascending=False)['total_harga']    

    # Tampilkan Grafik jika ada Data
    if jumlah_trx_lokal[0] > 0: 
        # Jumlah Transaksi Katalog Lokal OPD
        st.markdown('### Jumlah Transaksi OPD')
        kc1, kc2 = st.columns((3,7))
        with kc1:
            st.dataframe(opdtrxcount)
        with kc2:
            figkc = plt.figure(figsize=(10,6))
            sns.barplot(x = opdtrxcount, y = opdtrxcount.index)
            st.pyplot(figkc)

        # Nilai Transaksi Katalog Lokal OPD 
        st.markdown('### Nilai Transaksi OPD')
        ks1, ks2 = st.columns((3.3,6.7))
        with ks1:
            st.dataframe(opdtrxsum)
        with ks2:
            figks = plt.figure(figsize=(10,6))
            sns.barplot(x = opdtrxsum, y = opdtrxsum.index)
            st.pyplot(figks)
    else:
        st.error('BELUM ADA TRANSAKSI DI KATALOG LOKAL ...')

    # Download Data Button
    df1_download = convert_trxkatalog(df_kat_loc)
    df2_download = convert_prodkatalog(df_prod_loc)

    st.download_button(
        label = '📥 Download Data Transaksi E-KATALOG',
        data = df1_download,
        file_name = 'trxkatalog-' + kodeRUP + '.csv',
        mime = 'text/csv'
    )

    st.download_button(
        label = '📥 Download Data Produk E-KATALOG',
        data = df2_download,
        file_name = 'prodkatalog-' + kodeRUP + '.csv',
        mime = 'text/csv'
    )

## Tab Toko Daring
with tab2:
    
    ## Mulai Tampilkan Data Toko Daring
    st.subheader("TRANSAKSI TOKO DARING - " + pilih)

    jumlah_trx_daring = df_daring_loc['order_id'].value_counts().shape
    nilai_trx_daring = df_daring_loc['valuasi'].sum()
    nilai_trx_daring_print = format_currency(nilai_trx_daring, 'Rp. ', locale='id_ID')

    td1, td2 = st.columns(2)
    td1.metric("Jumlah Transaksi Toko Daring", jumlah_trx_daring[0])
    td2.metric("Nilai Transaksi Toko Daring", nilai_trx_daring_print)

    tmp_daring_loc = df_daring_loc[['nama_satker', 'order_id']]
    pv_daring_loc = tmp_daring_loc.pivot_table(
        index = ['nama_satker', 'order_id']
    )
    tmp_daring_loc_ok = pv_daring_loc.reset_index()
    opdtrxcount_daring = tmp_daring_loc_ok['nama_satker'].value_counts()
    opdtrxsum_daring = df_daring_loc.groupby(by='nama_satker').sum().sort_values(by='valuasi', ascending=False)['valuasi']  

        # Tampilkan Grafik jika ada Data
    if jumlah_trx_daring[0] > 0: 
        # Jumlah Transaksi Toko Daring OPD
        st.markdown('### Jumlah Transaksi Toko Daring OPD')
        tdc1, tdc2 = st.columns((4,6))
        with tdc1:
            st.dataframe(opdtrxcount_daring)
        with tdc2:
            figtdc = plt.figure(figsize=(10,6))
            sns.barplot(x = opdtrxcount_daring, y = opdtrxcount_daring.index)
            st.pyplot(figtdc)

        # Nilai Transaksi Katalog Lokal OPD 
        st.markdown('### Nilai Transaksi Toko Daring OPD')
        tds1, tds2 = st.columns((4,6))
        with tds1:
            st.dataframe(opdtrxsum_daring)
        with tds2:
            figtds = plt.figure(figsize=(10,6))
            sns.barplot(x = opdtrxsum_daring, y = opdtrxsum_daring.index)
            st.pyplot(figtds)
    else:
        st.error('BELUM ADA TRANSAKSI DI TOKO DARING ...')       

        # Download Data Button
    df1_download_daring = convert_trxdaring(df_daring_loc)

    st.download_button(
        label = '📥 Download Data Transaksi TOKO DARING',
        data = df1_download_daring,
        file_name = 'trxdaring-' + kodeRUP + '.csv',
        mime = 'text/csv'
    )