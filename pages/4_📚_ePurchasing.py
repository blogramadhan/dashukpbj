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
# Import library currency
from babel.numbers import format_currency
# Import library AgGrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Import library Google Cloud Storage
##from google.oauth2 import service_account
##from google.cloud import storage
# Import fungsi pribadi
from fungsi import *

# Setting CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Konfigurasi variabel lokasi UKPBJ
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

tahuns =    [2023, 2022]

pilih = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)
tahun = st.sidebar.selectbox("Pilih Tahun :", tahuns)

if pilih == "KAB. BENGKAYANG":
    kodeRUP = "D206"
    kodeFolder = "bky"
elif pilih == "KAB. KAPUAS HULU":
    kodeRUP = "D209"
    kodeFolder = "kph"
elif pilih == "KAB. KAYONG UTARA":
    kodeRUP = "D207"
    kodeFolder = "kku"
elif pilih == "KAB. KETAPANG":
    kodeRUP = "D201"
    kodeFolder = "ktp"
elif pilih == "KAB. KUBU RAYA":
    kodeRUP = "D202"
    kodeFolder = "kkr"
elif pilih == "KAB. LANDAK":
    kodeRUP = "D205"
    kodeFolder = "ldk"
elif pilih == "KAB. MELAWI":
    kodeRUP = "D210"
    kodeFolder = "mlw"
elif pilih == "KAB. MEMPAWAH":
    kodeRUP = "D552"
    kodeFolder = "mpw"
elif pilih == "KAB. SAMBAS":
    kodeRUP = "D208"
    kodeFolder = "sbs"
elif pilih == "KAB. SANGGAU":
    kodeRUP = "D204"
    kodeFolder = "sgu"
elif pilih == "KAB. SEKADAU":
    kodeRUP = "D198"
    kodeFolder = "skd"
elif pilih == "KAB. SINTANG":
    kodeRUP = "D211"
    kodeFolder = "stg"
elif pilih == "KOTA PONTIANAK":
    kodeRUP = "D199"
    kodeFolder = "ptk"
elif pilih == "KOTA SINGKAWANG":
    kodeRUP = "D200"
    kodeFolder = "skw"
elif pilih == "PROV. KALBAR":
    kodeRUP = "D197" 
    kodeFolder = "prov"

# Persiapan Dataset
## Google Cloud Storage
## Create API client.
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
#client = storage.Client(credentials=credentials)

# Ambil file dari Google Cloud Storage.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
#@st.experimental_memo(ttl=600)
#def unduh_df_parquet(bucket_name, file_path, destination):
#    bucket = client.bucket(bucket_name)
#    return bucket.blob(file_path).download_to_filename(destination)
##

## Dataset ePurchasing
con = duckdb.connect(database=':memory:')

#bucket = "dashukpbj"

### File path dan unduh file parquet dan simpan di memory - Lewat Google Cloud Storage
#DatasetKATALOG = f"epurchasing/epurchasing_gabung/katalogdetail{str(tahun)}.parquet"
#DatasetKATALOG_Temp = f"katalogdetail{str(tahun)}_temp.parquet"

#DatasetPRODUKKATALOG = f"epurchasing/epurchasing_gabung/prodkatalog{str(tahun)}.parquet"
#DatasetPRODUKKATALOG_Temp = f"prodkatalog{str(tahun)}_temp.parquet"

#DatasetTOKODARING = f"epurchasing/epurchasing_gabung/daring{str(tahun)}.parquet"
#DatasetTOKODARING_Temp = f"daring{str(tahun)}_temp.parquet"

### File path dan unduh file parquet dan simpan di memory - Lewat Google Cloud Storage via URL Public
DatasetKATALOG = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/epurchasing_gabung/katalogdetail{str(tahun)}.parquet"
#DatasetPRODUKKATALOG = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/epurchasing_gabung/prodkatalog{str(tahun)}.parquet"
DatasetPRODUKKATALOG = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/{kodeFolder}/prodkatalog{str(tahun)}.parquet"
DatasetTOKODARING = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/epurchasing_gabung/daring{str(tahun)}.parquet"

### Unduh data parquet KATALOG dan DARING
try:
    df_DatasetKATALOG = pd.read_parquet(DatasetKATALOG)
    df_katalog = con.execute(f"SELECT * FROM df_DatasetKATALOG WHERE kd_klpd = '{kodeRUP}' AND nama_satker IS NOT NULL").df()
except Exception:
    st.error("Dataset Transaksi Katalog Tidak Ada")

try:
    df_DatasetPRODUKKATALOG = pd.read_parquet(DatasetPRODUKKATALOG)
    #df_produk_katalog = con.execute(f"SELECT * FROM df_DatasetPRODUKKATALOG WHERE kd_klpd = '{kodeRUP}'").df()
    df_produk_katalog = con.execute(f"SELECT * FROM df_DatasetPRODUKKATALOG").df()
except Exception:
    st.error("Dataset Produk Katalog Tidak Ada")

# Buat Tab e-Katalog dan Toko Daring
tab1, tab2, tab3, tab4 = st.tabs(["| E-KATALOG |", "| TOKO DARING |", "| DETAIL E-KATALOG |", "| DETAIL TOKO DARING |"])

## Buat Tab ePurchasing
with tab1:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet E-Katalog
        #unduh_df_parquet(bucket, DatasetKATALOG, DatasetKATALOG_Temp)
        #unduh_df_parquet(bucket, DatasetPRODUKKATALOG, DatasetPRODUKKATALOG_Temp)
        #df_DatasetKATALOG = pd.read_parquet(DatasetKATALOG)
        #df_DatasetPRODUKKATALOG = pd.read_parquet(DatasetPRODUKKATALOG)
        #df_katalog = con.execute(f"SELECT * FROM read_parquet('{DatasetKATALOG_Temp}') WHERE kd_klpd = '{kodeRUP}' AND nama_satker IS NOT NULL").df()
        #df_produk_katalog = con.execute(f"SELECT * FROM read_parquet('{DatasetPRODUKKATALOG_Temp}') WHERE kd_klpd = '{kodeRUP}'").df()
        #df_katalog = con.execute(f"SELECT * FROM df_DatasetKATALOG WHERE kd_klpd = '{kodeRUP}' AND nama_satker IS NOT NULL").df()
        #df_produk_katalog = con.execute(f"SELECT * FROM df_DatasetPRODUKKATALOG WHERE kd_klpd = '{kodeRUP}'").df()

        # Query E-KATALOG
        df_katalog_lokal = con.execute(
            "SELECT * FROM df_katalog WHERE jenis_katalog = 'Lokal' AND nama_sumber_dana = 'APBD'"
        ).df()
        df_katalog_sektoral = con.execute(
            "SELECT * FROM df_katalog WHERE jenis_katalog = 'Sektoral'"
        ).df()
        df_katalog_nasional = con.execute(
            "SELECT * FROM df_katalog WHERE jenis_katalog = 'Nasional'"
        ).df()

        # Tab E-Katalog
        # Header dan Download Data Button
        download_katalog = unduh_data(df_katalog)
        download_produk_katalog = unduh_data(df_produk_katalog)

        d1, d2, d3 = st.columns((6,2,2))
        with d1:
            st.markdown(f"## **TRANSAKSI E-KATALOG - {pilih}**")
        with d2:
            st.download_button(
                label = '📥 Download Data Transaksi E-KATALOG',
                data = download_katalog,
                file_name = 'trxkatalog-' + kodeRUP + '.csv',
                mime = 'text/csv'
            )
        with d3:
            st.download_button(
                label = '📥 Download Data Produk E-KATALOG',
                data = download_produk_katalog,
                file_name = 'prodkatalog-' + kodeRUP + '.csv',
                mime = 'text/csv'
            )

        jumlah_produk = df_produk_katalog['nama_produk'].count()
        jumlah_penyedia = df_produk_katalog['nama_penyedia'].value_counts().shape

        jumlah_trx_lokal = df_katalog_lokal['no_paket'].value_counts().shape
        nilai_trx_lokal = df_katalog_lokal['total_harga'].sum()
        nilai_trx_lokal_print = format_currency(nilai_trx_lokal, 'Rp. ', locale='id_ID')

        jumlah_trx_sektoral = df_katalog_sektoral['no_paket'].value_counts().shape
        nilai_trx_sektoral = df_katalog_sektoral['total_harga'].sum()
        nilai_trx_sektoral_print = format_currency(nilai_trx_sektoral, 'Rp. ', locale='id_ID')

        jumlah_trx_nasional = df_katalog_nasional['no_paket'].value_counts().shape
        nilai_trx_nasional = df_katalog_nasional['total_harga'].sum()
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

        katalog_tabel_count_sql = """
            SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
            FROM df_katalog_lokal
            WHERE NAMA_SATKER IS NOT NULL
            GROUP BY NAMA_SATKER
            ORDER BY JUMLAH_TRANSAKSI DESC
        """
        katalog_tabel_sum_sql = """
            SELECT nama_satker AS NAMA_SATKER, SUM(total_harga) AS NILAI_TRANSAKSI
            FROM df_katalog_lokal
            WHERE NAMA_SATKER IS NOT NULL
            GROUP BY NAMA_SATKER
            ORDER BY NILAI_TRANSAKSI DESC
        """
        katalog_tabel_count = con.execute(katalog_tabel_count_sql).df()
        katalog_tabel_sum = con.execute(katalog_tabel_sum_sql).df()

        # Tampilkan Grafik jika ada Data
        if jumlah_trx_lokal[0] > 0: 

            # Jumlah Transaksi Katalog Lokal OPD
            st.markdown('### Jumlah Transaksi Katalog Lokal OPD')

            kc1, kc2 = st.columns((4,6))

            with kc1:

                gd = GridOptionsBuilder.from_dataframe(katalog_tabel_count)
                gd.configure_pagination()
                gd.configure_side_bar()
                gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

                gridOptions = gd.build()
                AgGrid(katalog_tabel_count, gridOptions=gridOptions, enable_enterprise_modules=True)

            with kc2:

                fig_katalog_count = px.bar(katalog_tabel_count, y='JUMLAH_TRANSAKSI', x='NAMA_SATKER', text_auto='.2s', title="Jumlah Transaksi Katalog Lokal")
                fig_katalog_count.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_katalog_count, theme="streamlit", use_container_width=True)             

            # Nilai Transaksi Katalog Lokal OPD 
            st.markdown('### Nilai Transaksi Katalog Lokal OPD')

            ks1, ks2 = st.columns((4,6))

            with ks1:

                gd = GridOptionsBuilder.from_dataframe(katalog_tabel_sum)
                gd.configure_pagination()
                gd.configure_side_bar()
                gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
                gd.configure_column("NILAI_TRANSAKSI", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})") 

                gridOptions = gd.build()
                AgGrid(katalog_tabel_sum, gridOptions=gridOptions, enable_enterprise_modules=True)

            with ks2:

                fig_katalog_sum = px.bar(katalog_tabel_sum, y='NILAI_TRANSAKSI', x='NAMA_SATKER', text_auto='.2s', title="Nilai Transaksi Toko Daring")
                fig_katalog_sum.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_katalog_sum, theme="streamlit", use_container_width=True)

        else:
            st.error('BELUM ADA TRANSAKSI DI KATALOG LOKAL ...')

    except Exception:
        st.error("Data Katalog Lokal belum ada ...")

## Tab Toko Daring
with tab2:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet Toko Daring
        #unduh_df_parquet(bucket, DatasetTOKODARING, DatasetTOKODARING_Temp)
        df_DatasetTOKODARING = pd.read_parquet(DatasetTOKODARING)
        #df_daring = con.execute(f"SELECT * FROM read_parquet('{DatasetTOKODARING_Temp}') WHERE kd_klpd = '{kodeRUP}' AND nama_satker IS NOT NULL").df()
        df_daring = con.execute(f"SELECT * FROM df_DatasetTOKODARING WHERE kd_klpd = '{kodeRUP}' AND nama_satker IS NOT NULL").df()

        # Tab Toko Daring
        st.markdown(f"## **TRANSAKSI TOKO DARING - {pilih}**")

        # Query Toko Daring
        jumlah_trx_daring = df_daring['order_id'].value_counts().shape
        nilai_trx_daring = df_daring['valuasi'].sum()
        nilai_trx_daring_print = format_currency(nilai_trx_daring, 'Rp. ', locale='id_ID')

        td1, td2 = st.columns(2)
        td1.metric("Jumlah Transaksi Toko Daring", jumlah_trx_daring[0])
        td2.metric("Nilai Transaksi Toko Daring", nilai_trx_daring_print)

        daring_tabel_count_sql = """
            SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(order_id)) AS JUMLAH_TRANSAKSI
            FROM df_daring
            GROUP BY nama_satker
            ORDER BY JUMLAH_TRANSAKSI DESC LIMIT 10
        """
        daring_tabel_sum_sql = """
            SELECT nama_satker AS NAMA_SATKER, SUM(valuasi) AS NILAI_TRANSAKSI
            FROM df_daring
            GROUP BY NAMA_SATKER
            ORDER BY NILAI_TRANSAKSI DESC LIMIT 10
        """
        daring_tabel_count = con.execute(daring_tabel_count_sql).df()
        daring_tabel_sum = con.execute(daring_tabel_sum_sql).df()

        # Tampilkan Grafik jika ada Data
        if jumlah_trx_daring[0] > 0: 

            # Jumlah Transaksi Toko Daring OPD
            st.markdown("### Jumlah Transaksi Toko Daring OPD")

            tdc1, tdc2 = st.columns((4,6))

            with tdc1:

                gd = GridOptionsBuilder.from_dataframe(daring_tabel_count)
                gd.configure_pagination()
                gd.configure_side_bar()
                gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

                gridOptions = gd.build()
                AgGrid(daring_tabel_count, gridOptions=gridOptions, enable_enterprise_modules=True)

            with tdc2:

                fig_daring_count = px.bar(daring_tabel_count, y='JUMLAH_TRANSAKSI', x='NAMA_SATKER', text_auto='.2s', title="Jumlah Transaksi Toko Daring")
                fig_daring_count.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_daring_count, theme="streamlit", use_container_width=True)

            # Nilai Transaksi Toko Daring OPD
            st.markdown("### Nilai Transaksi Toko Daring OPD")

            tds1, tds2 = st.columns((4,6))

            with tds1:

                gd = GridOptionsBuilder.from_dataframe(daring_tabel_sum)
                gd.configure_pagination()
                gd.configure_side_bar()
                gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
                gd.configure_column("NILAI_TRANSAKSI", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})") 

                gridOptions = gd.build()
                AgGrid(daring_tabel_sum, gridOptions=gridOptions, enable_enterprise_modules=True)

            with tds2:

                fig_daring_sum = px.bar(daring_tabel_sum, y='NILAI_TRANSAKSI', x='NAMA_SATKER', text_auto='.2s', title="Nilai Transaksi Toko Daring")
                fig_daring_sum.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_daring_sum, theme="streamlit", use_container_width=True)

        else:
            st.error("BELUM ADA TRANSAKSI DI TOKO DARING ...")       

        # Download Data Button
        download_daring = unduh_data(df_daring)

        st.download_button(
            label = '📥 Download Data Transaksi TOKO DARING',
            data = download_daring,
            file_name = 'trxdaring-' + kodeRUP + '.csv',
            mime = 'text/csv'
        )

    except Exception:
        st.error("Data Toko Daring belum ada ...")

with tab3:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet Detail Katalog
        #unduh_df_parquet(bucket, DatasetKATALOG, DatasetKATALOG_Temp)
        df_DatasetKATALOG = pd.read_parquet(DatasetKATALOG)
        #katalog_tab3 = con.execute(f"SELECT * FROM read_parquet('{DatasetKATALOG_Temp}') WHERE kd_klpd = '{kodeRUP}'").df()        
        katalog_tab3 = con.execute(f"SELECT * FROM df_DatasetKATALOG WHERE kd_klpd = '{kodeRUP}'").df()
        katalog_tabel_sql_tab3 = """
            SELECT nama_satker AS NAMA_SATKER, no_paket AS NOMOR_PAKET, nama_paket AS NAMA_PAKET, kd_rup AS KODE_RUP, nama_sumber_dana AS SUMBER_DANA, total_harga AS TOTAL_HARGA, paket_status_str AS STATUS_PAKET, nama_komoditas AS NAMA_KOMODITAS, jenis_katalog AS JENIS_KATALOG
            FROM katalog_tab3
        """
        katalog_tabel_tab3 = con.execute(katalog_tabel_sql_tab3).df()

        # Tab Detail Katalog OPD
        st.markdown(f"## **DETAIL E-KATALOG LOKAL TAHUN {tahun}**")

        gd = GridOptionsBuilder.from_dataframe(katalog_tabel_tab3)
        gd.configure_pagination()
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gd.configure_column("TOTAL_HARGA", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.TOTAL_HARGA.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})") 

        gridOptions = gd.build()
        AgGrid(katalog_tabel_tab3, gridOptions=gridOptions, enable_enterprise_modules=True)

    except Exception:
        st.error("Data Katalog belum ada, tabel tidak ditampilkan ...")

with tab4:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet Detail Toko Daring
        #unduh_df_parquet(bucket, DatasetTOKODARING, DatasetTOKODARING_Temp)
        df_DatasetTOKODARING = pd.read_parquet(DatasetTOKODARING)
        #daring = con.execute(f"SELECT * FROM read_parquet('{DatasetTOKODARING_Temp}') WHERE kd_klpd = '{kodeRUP}'").df()
        daring = con.execute(f"SELECT * FROM df_DatasetTOKODARING WHERE kd_klpd = '{kodeRUP}'").df()

        # Tab Detail Katalog OPD
        st.markdown(f"## **DETAIL TOKO DARING TAHUN {tahun}**")

        gd = GridOptionsBuilder.from_dataframe(daring)
        gd.configure_pagination()
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gd.configure_column("valuasi", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.valuasi.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})") 

        gridOptions = gd.build()
        AgGrid(daring, gridOptions=gridOptions, enable_enterprise_modules=True)

    except Exception:
        st.error("Data Toko Daring belum ada, tabel tidak ditampilkan ...")