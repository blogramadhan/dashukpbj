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

import streamlit as st

st.set_page_config(
    page_title="Dashboard UKPBJ",
    page_icon="👋",
    layout="wide"
)

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

st.title("Dashboard Pengadaan Barang dan Jasa")

st.markdown("""
*Dashboard* ini dibuat sebagai alat bantu untuk mempermudah para pelaku pengadaan di seluruh wilayah Provinsi Kalimantan Barat. Data yang disajikan, antara lain:

* **Rencana PBJ**
  * *RUP Daerah*
  * *Struktur Anggaran*
  * *RUP Perangkat Daerah*
  * *RUP Paket Penyedia*
  * *RUP Paket Swakelola*
* **Tender dan Seleksi**
  * Tender/Seleksi diumumkan
  * Tender/Seleksi Selesai
* ePurchasing
* Indeks Tata Kelola PBJ

*Made with love* dengan menggunakan bahasa programming [Python](https://www.python.org/) dengan beberapa *library* utama seperti:
* [Pandas](https://pandas.pydata.org/)
* [Streamlit](https://streamlit.io)
* [DuckDB](https://duckdb.org)

Sumber data dari *Dashboard* ini berasal dari **API JSON** yang ditarik harian dari [ISB LKPP](https://lkpp.go.id). Data tersebut kemudian disimpan di [Google Cloud Storage](https://google.com) untuk kemudian diolah lebih lanjut dengan [Python](https://python.org).

@2022 - **UlarKadut** 
""")

# Buat session pilihan UKPBJ
#daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
#            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
#            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

#if "ukpbj" not in st.session_state:
#    st.session_state["ukpbj"] = ""

#ukpbj = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)

#st.session_state["ukpbj"] = ukpbj