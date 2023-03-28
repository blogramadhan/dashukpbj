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
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Konfigurasi variabel lokasi UKPBJ
daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

tahuns = [2022, 2023]

pilih = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)
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

# Persiapan Dataset
## Google Cloud Storage
## Create API Client
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
#client = storage.Client(credentials=credentials)

# Ambil file dari Google Cloud Storage.
# Uses st.experimental_memo to only rerun when the query changes or after 10 menit
#@st.experimental_memo(ttl=600)
#def unduh_df_parquet(bucket_name, file_path, destination):
#    bucket = client.bucket(bucket_name)
#    return bucket.blob(file_path).download_to_filename(destination)
##

## Dataset SIRUP
con = duckdb.connect(database=':memory:')

#bucket = "dashukpbj"

### File path dan unduh file parquet untuk disimpan di memory - Lewat Google Cloud Storage
#DatasetTENDERDTP = f"itkp/{kodeFolder}/dtender_dtp{str((tahun))}.parquet"
#DatasetTENDERDTP_Temp = f"dtender_dtp{kodeFolder}{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetTENDERDTP, DatasetTENDERDTP_Temp)

#DatasetTENDERDTS = f"itkp/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
#DatasetTENDERDTS_Temp = f"dtender_dts{kodeFolder}{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetTENDERDTS, DatasetTENDERDTS_Temp)

#DatasetSIRUPDP = f"itkp/{kodeFolder}/sirupdp{str(tahun)}.parquet"
#DatasetSIRUPDP_Temp = f"sirupdp{kodeFolder}{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetSIRUPDP, DatasetSIRUPDP_Temp)

#DatasetSIRUPDSARSAP = f"itkp/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
#DatasetSIRUPDSARSAP_Temp = f"sirupdsa_rsap{kodeFolder}{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetSIRUPDSARSAP, DatasetSIRUPDSARSAP_Temp)

### File path dan unduh file parquet dan simpan di memory - Lewat Google Cloud Storage via URL Public
#DatasetTENDERDTP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dtp{str(tahun)}.parquet"
#DatasetTENDERDTS = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
DatasetSIRUPDP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/sirupdp{str(tahun)}.parquet"
DatasetSIRUPDSARSAP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"

### Query dataframe parquet penting
#df_dtp = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTP_Temp}')").df()
#df_dts = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTS_Temp}')").df()
#df_SIRUPDP = con.execute(f"SELECT namasatker FROM read_parquet('{DatasetSIRUPDP_Temp}')").df()
#df_SIRUPDSARSAP = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPDSARSAP_Temp}')").df()
df_SIRUPDP = pd.read_parquet(DatasetSIRUPDP)
df_SIRUPDSARSAP = pd.read_parquet(DatasetSIRUPDSARSAP)

### Query Data Tender dan Non Tender

#### Buat variabel nama satker unik
df_rsap = con.execute("SELECT * FROM df_SIRUPDSARSAP").df()

### Buat variabel nama satker unik
#namaopd = df_rsap['nama_satker'].unique()
namaopd = df_SIRUPDP['namasatker'].unique()

##########
tab1, tab2 = st.tabs(["| TENDER/SELEKSI DIUMUMKAN |", "| TENDER/SELEKSI SELESAI |"])

with tab1:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet Tender Berjalan
        #unduh_df_parquet(bucket, DatasetTENDERDTP, DatasetTENDERDTP_Temp)
        DatasetTENDERDTP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dtp{str(tahun)}.parquet"
        #df_dtp = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTP_Temp}')").df()
        df_dtp = pd.read_parquet(DatasetTENDERDTP)

        # Tab TENDER/SELEKSI DIUMUMKAN
        st.markdown(f"## **TENDER/SELEKSI DIUMUMKAN TAHUN {tahun}**")

        ### Tampilan pilihan menu nama opd
        opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='tab1')

        dtp_tabel = con.execute(f"SELECT * FROM df_dtp WHERE nama_satker = '{opd}'").df()
        dtp_tabel_tampil = con.execute(
            "SELECT kd_rup_paket AS KODE_RUP, nama_paket AS NAMA_PAKET, mtd_pemilihan AS METODE_PEMILIHAN, pagu AS PAGU, tgl_buat_paket AS TGL_BUAT, tgl_pengumuman_tender AS TGL_RENC_TENDER, nama_status_tender AS STATUS_PAKET FROM dtp_tabel"
        ).df()

        ### Tampilan Data Tender Diumumkan Perangkat Daerah
        unduh_dtp = unduh_data(dtp_tabel)

        dtp1, dtp2 = st.columns((8,2))

        with dtp1:
            st.markdown(f"### **{opd}**")
        with dtp2:
            st.download_button(
                label = "📥 Download Data Tender Diumumkan",
                data = unduh_dtp,
                file_name = f"datatenderumumkan-{opd}.csv",
                mime = "text/csv"                
            )

        ### Tabulasi data dan pagination AgGrid
        gd = GridOptionsBuilder.from_dataframe(dtp_tabel_tampil)
        gd.configure_pagination()
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gd.configure_column("PAGU", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.PAGU.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})") 

        gridOptions = gd.build()
        AgGrid(dtp_tabel_tampil, gridOptions=gridOptions, enable_enterprise_modules=True)

    except Exception:
        st.error("Data tender/seleksi berjalan belum ada, tabel tidak ditampilkan ...")

with tab2:

    ### Gunakan Try dan Except untuk pilihan logika
    try:
        # Unduh data parquet Tender Selesai
        #unduh_df_parquet(bucket, DatasetTENDERDTS, DatasetTENDERDTS_Temp)
        DatasetTENDERDTS = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
        #df_dts = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTS_Temp}')").df()
        df_dts = pd.read_parquet(DatasetTENDERDTS)

        # Tab TENDER/SELEKSI DIUMUMKAN
        st.markdown(f"## **TENDER/SELEKSI SELESAI TAHUN {tahun}**")

        ### Tampilan pilihan menu nama opd
        opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='tab2')

        dtp_tabel = con.execute(f"SELECT * FROM df_dtp WHERE nama_satker = '{opd}'").df()
        dts_tabel = con.execute(f"SELECT * FROM df_dts WHERE nama_satker = '{opd}'").df()
        dts_tabel_gab = con.execute(
            "SELECT * FROM dtp_tabel AS dtp JOIN dts_tabel AS dts ON dtp.kd_rup_paket = dts.kd_rup_paket"
        ).df()
        dts_tabel_gab_tampil = con.execute(
            "SELECT dts.kd_rup_paket AS KODE_RUP, dtp.nama_paket AS NAMA_PAKET, dtp.mtd_pemilihan AS METODE_PEMILIHAN, dtp.kualifikasi_paket AS KUALIFIKASI_PAKET, dts.nilai_kontrak AS NILAI_KONTRAK, dts.tgl_pengumuman_tender AS TGL_UMUMKAN, dts.tgl_penetapan_pemenang AS TGL_MENANG, dts.nama_penyedia AS NAMA_PEMENANG FROM dtp_tabel AS dtp JOIN dts_tabel AS dts ON dtp.kd_rup_paket = dts.kd_rup_paket"
        ).df()

        ### Tampilan Data Tender Selesai Perangkat Daerah
        unduh_dts_gab = unduh_data(dts_tabel_gab)

        dts1, dts2 = st.columns((8,2))
        with dts1:
            st.markdown(f"### **{opd}**")
        with dts2:
            st.download_button(
                label = "📥 Download Data Tender Diumumkan",
                data = unduh_dts_gab,
                file_name = f"datatenderselesai-{opd}.csv",
                mime = "text/csv"                
            )

        ### Tabulasi data dan pagination AgGrid
        gd = GridOptionsBuilder.from_dataframe(dts_tabel_gab_tampil)
        gd.configure_pagination()
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gd.configure_column("NILAI_KONTRAK", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], valueGetter = "data.NILAI_KONTRAK.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")

        gridOptions = gd.build()
        AgGrid(dts_tabel_gab_tampil, gridOptions=gridOptions, enable_enterprise_modules=True)

    except Exception:
        st.error("Data tender/seleksi selesai belum ada, tabel tidak ditampilkan ...")