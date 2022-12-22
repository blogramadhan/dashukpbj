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
import plotly.express as px

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

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    return bucket.blob(file_path).download_as_string().decode("utf-8")
 
#################
# Dataframe GCS #
#################
bucket_name = "ular_kadut"

con = duckdb.connect()
#DatasetSIRUPDP_Path = "sirupdp2023.parquet"
#DatasetSIRUPDP = read_file(bucket_name, DatasetSIRUPDP_Path)
#df_pp_umumkan = con.execute(
#    f"SELECT * FROM '{DatasetSIRUPDP}' WHERE statusumumkan = 'Terumumkan'"
#).df()
#df_mp_hitung = con.execute(
#    "SELECT metodepengadaan AS METODE_PENGADAAN, COUNT(metodepengadaan) AS JUMLAH_PAKET FROM df_pp_umumkan WHERE metodepengadaan IS NOT NULL GROUP BY metodepengadaan;"
#).df()

#################
file_path = "myfile.csv"
content = read_file(bucket_name, file_path)
content_print = con.execute(f"SELECT * FROM {content}").df()
#################

st.markdown("## Tes Google Cloud Storage")
# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")

#st.markdown("## Data SIRUP")
#st.table(content_print)
