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
from st_aggrid import AgGrid, JsCode
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

tahuns = [2023, 2022]

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
## Create API client.
#redentials = service_account.Credentials.from_service_account_info(
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

## Dataset ITKP UKPBJ
con = duckdb.connect(database=':memory:')

#bucket = "dashukpbj"

### File path dan unduh file parquet dan simpan di memory - Lewat Google Cloud Storage
#DatasetSIRUPDP = f"itkp/{kodeFolder}/sirupdp{str(tahun)}.parquet"
#DatasetSIRUPDP_Temp = f"sirupdp{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetSIRUPDP, DatasetSIRUPDP_Temp)

#DatasetSIRUPSW = f"itkp/{kodeFolder}/sirupdsw{str(tahun)}.parquet"
#DatasetSIRUPSW_Temp = f"sirupdsw{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetSIRUPSW, DatasetSIRUPSW_Temp)

#DatasetSIRUPDSARSAP = f"itkp/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
#DatasetSIRUPDSARSAP_Temp = f"sirupdsa_rsap{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetSIRUPDSARSAP, DatasetSIRUPDSARSAP_Temp)

#DatasetTENDERDTS = f"itkp/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
#DatasetTENDERDTS_Temp = f"dtender_dts{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetTENDERDTS, DatasetTENDERDTS_Temp)

#DatasetTENDERDTKS = f"itkp/{kodeFolder}/dtender_dtks{str(tahun)}.parquet"
#atasetTENDERDTKS_Temp = f"dtender_dtks{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetTENDERDTKS, DatasetTENDERDTKS_Temp)

#DatasetNTENDERDNTS = f"itkp/{kodeFolder}/dntender_dnts{str(tahun)}.parquet"
#DatasetNTENDERDNTS_Temp = f"dntenter_dnts{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetNTENDERDNTS, DatasetNTENDERDNTS_Temp)

#DatasetKATALOG = f"epurchasing/{kodeFolder}/trxkatalog{str(tahun)}.parquet"
#DatasetKATALOG_Temp = f"trxkatalog{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetKATALOG, DatasetKATALOG_Temp)

#DatasetDARING = f"epurchasing/{kodeFolder}/daring{str(tahun)}.parquet"
#DatasetDARING_Temp = f"daring{str(tahun)}_temp.parquet"
#unduh_df_parquet(bucket, DatasetDARING, DatasetDARING_Temp)

### File path dan unduh file parquet dan simpan di memory - Lewat Google Cloud Storage via URL Public
DatasetSIRUPDP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/sirupdp{str(tahun)}.parquet"
DatasetSIRUPDSW = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/sirupdsw{str(tahun)}.parquet"
DatasetSIRUPDSARSAP = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
DatasetTENDERDTS = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
DatasetTENDERDTKS= f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dtender_dtks{str(tahun)}.parquet"
DatasetNTENDERDNTS = f"https://storage.googleapis.com/dashukpbj_asia/itkp/{kodeFolder}/dntender_dnts{str(tahun)}.parquet"
DatasetKATALOG = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/{kodeFolder}/trxkatalog{str(tahun)}.parquet"
DatasetDARING = f"https://storage.googleapis.com/dashukpbj_asia/epurchasing/{kodeFolder}/daring{str(tahun)}.parquet"

### Query dataframe parquet penting
#### Data Paket Penyedia dan Swakelola
df_DatasetSIRUPDP = pd.read_parquet(DatasetSIRUPDP)
df_DatasetSIRUPDSW = pd.read_parquet(DatasetSIRUPDSW)
#df_pp = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPDP_Temp}')").df()
#df_sw = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPSW_Temp}')").df()
df_pp = con.execute(f"SELECT * FROM df_DatasetSIRUPDP").df()
df_sw = con.execute(f"SELECT * FROM df_DatasetSIRUPDSW").df()
#### Data Struktur Anggaran
df_DatasetSIRUPDSARSAP = pd.read_parquet(DatasetSIRUPDSARSAP)
#df_rsap = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPDSARSAP_Temp}')").df()
df_rsap = con.execute(f"SELECT * FROM df_DatasetSIRUPDSARSAP").df()
#### Data Tender
df_DatasetTENDERDTS = pd.read_parquet(DatasetTENDERDTS)
df_DatasetTENDERDTKS = pd.read_parquet(DatasetTENDERDTKS)
#df_dts = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTS_Temp}')").df()
#df_dtks = con.execute(f"SELECT * FROM read_parquet('{DatasetTENDERDTKS_Temp}')").df()
df_dts = con.execute(f"SELECT * FROM df_DatasetTENDERDTS").df()
df_dtks = con.execute(f"SELECT * FROM df_DatasetTENDERDTKS").df()
#### Data Non Tender
df_DatasetNTENDERDNTS = pd.read_parquet(DatasetNTENDERDNTS)
#df_dnts = con.execute(f"SELECT * FROM read_parquet('{DatasetNTENDERDNTS_Temp}')").df()
df_dnts = con.execute(f"SELECT * FROM df_DatasetNTENDERDNTS").df()
#### Data Katalog
df_DatasetKATALOG = pd.read_parquet(DatasetKATALOG)
#df_katalog = con.execute(f"SELECT * FROM read_parquet('{DatasetKATALOG_Temp}')").df()
df_katalog = con.execute(f"SELECT * FROM df_DatasetKATALOG").df()
#### Data Daring
df_DatasetDARING = pd.read_parquet(DatasetDARING)
#df_daring = con.execute(f"SELECT * FROM read_parquet('{DatasetDARING_Temp}')").df()
df_daring = con.execute(f"SELECT * FROM df_DatasetDARING").df()

### Query Data RUP paket penyedia
df_pp_umumkan = df_pp[df_pp['statusumumkan'].isin(['Terumumkan'])]
df_pp_belum_umumkan = df_pp[df_pp['statusumumkan'].isin(['Draf', 'Draf Lengkap', 'Final Draft'])]
df_pp_umumkan_umk = df_pp_umumkan[df_pp_umumkan['statususahakecil'] == 'UsahaKecil']
df_pp_umumkan_pdn = df_pp_umumkan[df_pp_umumkan['statuspdn'] == 'PDN']

df_pp_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender', 'Tender Cepat', 'Seleksi'])]
df_pp_tender = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender'])]
df_pp_tender_cepat = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender Cepat'])]
df_pp_seleksi = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Seleksi'])]

df_pp_non_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung', 'Penunjukan Langsung'])]
df_pp_pengadaan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung'])]
df_pp_penunjukan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Penunjukan Langsung'])]

df_pp_epurchasing = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['e-Purchasing'])]

### Query Data RUP paket swakelola
df_sw_umumkan = df_sw[df_sw['statusumumkan'] == 'Terumumkan']
df_sw_inisiasi = df_sw[df_sw['statusumumkan'] == 'Terinisiasi']

######### 

# Buat tab ITKP UKPBJ dan ITKP Perangkat Daerah
tab1, tab2, tab3 = st.tabs(["SIRUP", "E-TENDERING", "NON E-TENDERING"])

with tab1:
    # Tab pemanfaatan SIRUP

    ### Tampilan pemanfaatan SIRUP
    st.markdown(f"## **PEMANFAATAN SIRUP - {tahun}**")

    ### RUP struktur anggaran
    st.markdown("### Struktur Anggaran")
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

    ### Posisi input RUP
    st.markdown("### Posisi Input RUP")
    jumlah_total_rup = df_pp_umumkan.shape[0] + df_sw_umumkan.shape[0]
    nilai_total_rup = df_pp_umumkan['jumlahpagu'].sum() + df_sw_umumkan['jumlahpagu'].sum()
    nilai_total_rup_print = format_currency(nilai_total_rup, 'Rp. ', locale='id_ID')

    pir1, pir2, pir3 = st.columns(3)
    pir1.metric("", "Jumlah Total")
    pir2.metric("Jumlah Total Paket RUP", jumlah_total_rup)
    pir3.metric("Nilai Total Paket RUP", nilai_total_rup_print)

    jumlah_rup_umumkan = df_pp_umumkan.shape[0]
    nilai_rup_umumkan = df_pp_umumkan['jumlahpagu'].sum()
    nilai_rup_umumkan_print = format_currency(nilai_rup_umumkan, 'Rp. ', locale='id_ID')

    pirpp1, pirpp2, pirpp3 = st.columns(3)
    pirpp1.metric("","Paket Penyedia")
    pirpp2.metric("Jumlah Total Paket RUP", jumlah_rup_umumkan)
    pirpp3.metric("Nilai Total Paket RUP", nilai_rup_umumkan_print)

    jumlah_rup_sw_umumkan = df_sw_umumkan.shape[0]
    nilai_rup_sw_umumkan = df_sw_umumkan['jumlahpagu'].sum()
    nilai_rup_sw_umumkan_print = format_currency(nilai_rup_sw_umumkan, 'Rp. ', locale='id_ID')

    pirsw1, pirsw2, pirsw3 = st.columns(3)
    pirsw1.metric("", "Paket Swakelola")
    pirsw2.metric("Jumlah Total Paket RUP", jumlah_rup_sw_umumkan)
    pirsw3.metric("Nilai Total paket RUP", nilai_rup_sw_umumkan_print)

    ### Persentase input RUP
    persen_capaian_rup = (nilai_total_rup / belanja_pengadaan)
    persen_capaian_rup_print = "{:.2%}".format(persen_capaian_rup)

    pr1, pr2, pr3 = st.columns(3)
    #pr1.metric("", "")
    pr2.metric("", "Persentase Capaian RUP")
    pr3.metric("Persentase Capaian RUP", persen_capaian_rup_print)

with tab2:
    # Tab pemanfaatan e-Tendering

    ### Tampilan Pemanfaatan e-Tendering
    st.markdown(f"## **PEMANFAATAN E-TENDERING - {tahun}**")

    ### Pengumuman e-Tendering
    st.markdown("### Pengumuman e-Tendering")

    jumlah_total_etendering = df_pp_etendering.shape[0]
    nilai_total_etendering = df_pp_etendering['jumlahpagu'].sum()
    nilai_total_etendering_print = format_currency(nilai_total_etendering, 'Rp. ', locale='id_ID')

    et1, et2, et3 = st.columns(3)
    et1.metric("", "Jumlah Total")
    et2.metric("Jumlah Total e-Tendering", jumlah_total_etendering)
    et3.metric("Nilai Total e-Tendering", nilai_total_etendering_print)

    jumlah_etendering_tender = df_pp_tender.shape[0]
    nilai_etendering_tender = df_pp_tender['jumlahpagu'].sum()
    nilai_etendering_tender_print = format_currency(nilai_etendering_tender, 'Rp. ', locale='id_ID')

    ett1, ett2, ett3 = st.columns(3)
    ett1.metric("", "e-Tendering (Tender)")
    ett2.metric("Jumlah e-Tendering (Tender)", jumlah_etendering_tender)
    ett3.metric("Nilai e-Tendering (Tender)", nilai_etendering_tender_print)

    jumlah_etendering_tender_cepat = df_pp_tender_cepat.shape[0]
    nilai_etendering_tender_cepat = df_pp_tender_cepat['jumlahpagu'].sum()
    nilai_etendering_tender_cepat_print = format_currency(nilai_etendering_tender_cepat, 'Rp. ', locale='id_ID')

    ettc1, ettc2, ettc3 = st.columns(3)
    ettc1.metric("", "e-Tendering (Tender Cepat)")
    ettc2.metric("Jumlah e-Tendering (Tender Cepat", jumlah_etendering_tender_cepat)
    ettc3.metric("Nilai e-Tendering (Tender Cepat)", nilai_etendering_tender_cepat_print)

    jumlah_etendering_seleksi = df_pp_seleksi.shape[0]
    nilai_etendering_seleksi = df_pp_seleksi['jumlahpagu'].sum()
    nilai_etendering_seleksi_print = format_currency(nilai_etendering_seleksi, 'Rp. ', locale='id_ID')

    ets1, ets2, ets3 = st.columns(3)
    ets1.metric("", "e-Tendering (Seleksi)")
    ets2.metric("Jumlah e-Tendering (Seleksi)", jumlah_etendering_seleksi)
    ets3.metric("Nilai e-Tendering (Seleksi)", nilai_etendering_seleksi_print) 

    ### Realisasi e-Tendering
    st.markdown("### Realisasi e-Tendering")

    jumlah_total_realisasi_etendering = df_dts.shape[0]
    nilai_total_realisasi_etendering = df_dts['pagu'].sum()
    nilai_total_realisasi_etendering_print = format_currency(nilai_total_realisasi_etendering, 'Rp. ', locale='id_ID')

    ret1, ret2, ret3 = st.columns(3)
    ret1.metric("", "Realisasi E-Tendering")
    ret2.metric("Jumlah Total Realisasi E-Tendering", jumlah_total_realisasi_etendering)
    ret3.metric("Nilai Total Realisasi E-Tendering", nilai_total_realisasi_etendering_print)           

    ### Persentase e-Tendering
    st.markdown("### Persentase e-Tendering")

    persen_capaian_etendering = (nilai_total_realisasi_etendering / nilai_total_etendering)
    persen_capaian_etendering_print = "{:.2%}".format(persen_capaian_etendering)

    pe1, pe2, pe3 = st.columns(3)
    pe1.metric("", "")
    pe2.metric("", "Persentase E-Tendering")
    pe3.metric("Persentase E-Tendering", persen_capaian_etendering_print)

with tab3:
    # Tab pemanfaatan non e-Tendering

    ### Tampilan pemanfaatan non e-Tendering
    st.markdown(f"## **PEMANFAATAN NON E-TENDERING - {tahun}**")

    ### Pengumuman non e-Tendering
    st.markdown("### Pengumuman non e-Tendering")

    jumlah_total_non_etendering = df_pp_non_etendering.shape[0]
    nilai_total_non_etendering = df_pp_non_etendering['jumlahpagu'].sum()
    nilai_total_non_etendering_print = format_currency(nilai_total_non_etendering, 'Rp. ', locale='id_ID')

    net1, net2, net3 = st.columns(3)
    net1.metric("", "Jumlah Total")
    net2.metric("Jumlah Total Non E-Tendering", jumlah_total_non_etendering)
    net3.metric("Nilai Total Non E-Tendering", nilai_total_non_etendering_print)

    jumlah_pengadaan_langsung = df_pp_pengadaan_langsung.shape[0]
    nilai_pengadaan_langsung = df_pp_pengadaan_langsung['jumlahpagu'].sum()
    nilai_pengadaan_langsung_print = format_currency(nilai_pengadaan_langsung, 'Rp. ', locale='id_ID')

    netpl1, netpl2, netpl3 = st.columns(3)
    netpl1.metric("", "Pengadaan Langsung")
    netpl2.metric("Jumlah Non E-Tendering (Pengadaan Langsung)", jumlah_pengadaan_langsung)
    netpl3.metric("Nilai Non E-Tendering (Pengadaan Langsung)", nilai_pengadaan_langsung_print)

    jumlah_penunjukan_langsung = df_pp_penunjukan_langsung.shape[0]
    nilai_penunjukan_langsung = df_pp_penunjukan_langsung['jumlahpagu'].sum()
    nilai_penunjukan_langsung_print = format_currency(nilai_penunjukan_langsung, 'Rp. ', locale='id_ID')

    netpnl1, netpnl2, netpnl3 = st.columns(3)
    netpnl1.metric("", "Penunjukan Langsung")
    netpnl2.metric("Jumlah Non E-Tendering (Penunjukan Langsung)", jumlah_penunjukan_langsung)
    netpnl3.metric("Nilai Non E-Tendering (Penunjukan Langsung)", nilai_penunjukan_langsung_print)