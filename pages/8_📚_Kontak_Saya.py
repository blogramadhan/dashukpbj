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
import streamlit as st
import duckdb
import pandas as pd

from google.oauth2 import service_account
from google.cloud import storage


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

st.title("Kontak Saya")

#### Tes Google Cloud Storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def download_to_local_file(bucket_name, file_path, destination):
    bucket = client.bucket(bucket_name)
    return bucket.blob(file_path).download_to_filename(destination)

bucket = "dashukpbj"
file_sirupdp = "data/sirupdp2023.parquet"
file_sirupdp_temp = "sirupdp2023_temp.parquet"
file_sirupdsw = "data/sirupdsw2023.parquet"
file_sirupdsw_temp = "sirupdsw2023_temp.parquet"

download_to_local_file(
    bucket, file_sirupdp, file_sirupdp_temp
)
download_to_local_file(
    bucket, file_sirupdsw, file_sirupdsw_temp
)

con = duckdb.connect(database=':memory:')
rupdp = con.execute(f"SELECT namasatker, namapaket, jumlahpagu FROM read_parquet('{file_sirupdp_temp}') LIMIT 5").df()
rupdsw = con.execute(f"SELECT namasatker, namapaket, jumlahpagu FROM read_parquet('{file_sirupdsw_temp}') LIMIT 2").df()
st.dataframe(rupdp)
st.dataframe(rupdsw)