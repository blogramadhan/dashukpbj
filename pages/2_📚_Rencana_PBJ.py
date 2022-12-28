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
from google.oauth2 import service_account
from google.cloud import storage
# Import fungsi pribadi
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
## Create API Client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Ambil file dari Google Cloud Storage.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def unduh_df_parquet(bucket_name, file_path, destination):
    bucket = client.bucket(bucket_name)
    return bucket.blob(file_path).download_to_filename(destination)
##

## Dataset SIRUP
con = duckdb.connect(database=':memory:')

bucket = "dashukpbj"

### File path dan unduh file parquet dan simpan di memory
DatasetSIRUPDP = f"itkp/{kodeFolder}/sirupdp{str(tahun)}.parquet"
DatasetSIRUPDP_Temp = f"sirupdp{kodeFolder}{str(tahun)}_temp.parquet"
unduh_df_parquet(bucket, DatasetSIRUPDP, DatasetSIRUPDP_Temp)

DatasetSIRUPSW = f"itkp/{kodeFolder}/sirupdsw{str(tahun)}.parquet"
DatasetSIRUPSW_Temp = f"sirupdsw{kodeFolder}{str(tahun)}_temp.parquet"
unduh_df_parquet(bucket, DatasetSIRUPSW, DatasetSIRUPSW_Temp)

DatasetSIRUPDSARSAP = f"itkp/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
DatasetSIRUPDSARSAP_Temp = f"sirupdsa_rsap{kodeFolder}{str(tahun)}_temp.parquet"
unduh_df_parquet(bucket, DatasetSIRUPDSARSAP, DatasetSIRUPDSARSAP_Temp)

### Query dataframe parquet penting 
df_SIRUPDP = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPDP_Temp}')").df()
df_SIRUPSW = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPSW_Temp}')").df()
df_SIRUPDSARSAP = con.execute(f"SELECT * FROM read_parquet('{DatasetSIRUPDSARSAP_Temp}')").df()

##########

### Query Data RUP paket penyedia
df_pp_umumkan = con.execute("SELECT * FROM df_SIRUPDP WHERE statusumumkan = 'Terumumkan'").df()
df_pp_belum_umumkan = con.execute("SELECT * FROM df_SIRUPDP WHERE statusumumkan IN ('Draf','Draf Lengkap','Final Draft')").df()
df_pp_umumkan_umk = con.execute("SELECT * FROM df_pp_umumkan WHERE statususahakecil = 'UsahaKecil'").df()
df_pp_umumkan_pdn = con.execute("SELECT * FROM df_pp_umumkan WHERE statuspdn = 'PDN'").df()

df_pp_etendering = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan IN ('Tender','Tender Cepat','Seleksi')").df()
df_pp_tender = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'Tender'").df()
df_pp_tender_cepat = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'Tender Cepat'").df()
df_pp_seleksi = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'Seleksi'").df()

df_pp_non_etendering = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan IN ('Pengadaan Langsung','Penunjukan Langsung')").df()
df_pp_pengadaan_langsung = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'Pengadaan Langsung'").df()
df_pp_penunjukan_langsung = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'Penunjukan Langsung'").df()

df_pp_epurchasing = con.execute("SELECT * FROM df_pp_umumkan WHERE metodepengadaan = 'e-Purchasing'").df()

### Data RUP paket swakelola
df_sw_umumkan = con.execute("SELECT * FROM df_SIRUPSW WHERE statusumumkan = 'Terumumkan'").df()
df_sw_inisiasi = con.execute("SELECT * FROM df_SIRUPSW WHERE statusumumkan = 'Terinisiasi'").df()

### Data struktur anggaran RUP
df_rsap = con.execute("SELECT * FROM df_SIRUPDSARSAP").df()
#### Buat variabel nama satker unik
namaopd = df_rsap['nama_satker'].unique()

#########

# Buat tab ITKP UKPBJ dan ITKP Perangkat Daerah
tab1, tab2, tab3, tab4, tab5 = st.tabs(["| RUP DAERAH |", "| STRUKTUR ANGGARAN |", "| RUP PERANGKAT DAERAH |", "| RUP PAKET PENYEDIA |", "| RUP PAKET SWAKELOLA |"])

with tab1:
    # Tab pemanfaatan SIRUP

    # Dataset
    df_mp_hitung = con.execute(f"SELECT metodepengadaan AS METODE_PENGADAAN, COUNT(metodepengadaan) AS JUMLAH_PAKET FROM df_pp_umumkan WHERE metodepengadaan IS NOT NULL GROUP BY metodepengadaan").df()
    df_mp_nilai = con.execute(f"SELECT metodepengadaan AS METODE_PENGADAAN, SUM(jumlahpagu) AS NILAI_PAKET FROM df_pp_umumkan WHERE metodepengadaan IS NOT NULL GROUP BY metodepengadaan").df()
    df_jp_hitung = con.execute(f"SELECT jenispengadaan AS JENIS_PENGADAAN, COUNT(jenispengadaan) AS JUMLAH_PAKET FROM df_pp_umumkan WHERE jenispengadaan IS NOT NULL GROUP BY jenispengadaan").df()
    df_jp_nilai = con.execute(f"SELECT jenispengadaan AS JENIS_PENGADAAN, SUM(jumlahpagu) AS NILAI_PAKET FROM df_pp_umumkan WHERE jenispengadaan IS NOT NULL GROUP BY jenispengadaan").df()

    ### Tampilan pemanfaatan SIRUP
    unduh_rupdp = unduh_data(df_pp_umumkan)
    unduh_rupsw = unduh_data(df_sw_umumkan)

    d1, d2, d3 = st.columns((6,2,2))
    with d1:
        st.markdown(f"## **RUP - {pilih} - {tahun}**")
    with d2:
        st.download_button(
            label = "📥 Download RUP Penyedia",
            data = unduh_rupdp,
            file_name = f"ruppenyedia-{kodeFolder}.csv",
            mime = "text/csv"            
        )
    with d3:
         st.download_button(
            label = "📥 Download RUP Swakelola",
            data = unduh_rupsw,
            file_name = f"rupswakelola-{kodeFolder}.csv",
            mime = "text/csv"            
        )       

    ### RUP struktur anggaran
    st.markdown("### Struktur Anggaran")
    belanja_pengadaan = df_rsap['belanja_pengadaan'].sum()
    belanja_pengadaan_print = format_currency(belanja_pengadaan, 'Rp. ', locale='id_ID')
    belanja_operasional = df_rsap['belanja_operasi'].sum()
    belanja_operasional_print = format_currency(belanja_operasional, 'Rp. ', locale='id_ID')
    belanja_modal = df_rsap['belanja_modal'].sum()
    belanja_modal_print = format_currency(belanja_modal, 'Rp. ', locale='id_ID')
    belanja_total = df_rsap['total_belanja'].sum()
    belanja_total_print = format_currency(belanja_total, 'Rp. ', locale='id_ID')

    sa1, sa2, sa3, sa4 = st.columns(4)
    sa1.metric("Belanja Pengadaan", belanja_pengadaan_print)
    sa2.metric("Belanja Operasional", belanja_operasional_print)
    sa3.metric("Belanja Modal", belanja_modal_print)
    sa4.metric("Belanja Total", belanja_total_print)

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
    pr1.metric("", "")
    pr2.metric("", "Persentase Capaian RUP")
    pr3.metric("Persentase Capaian RUP", persen_capaian_rup_print)

    ### Metode dan Jenis Pengadaan
    st.markdown("### Metode Pengadaan")
    mph1, mph2 = st.columns((5,5))
    with mph1:
        st.markdown("#### Berdasarkan Jumlah Paket")
        AgGrid(df_mp_hitung)
    with mph2:
        st.markdown("#### Berdasarkan Nilai Paket")
        AgGrid(df_mp_nilai)
 
    mpn1, mpn2 = st.columns((5,5))
    with mpn1:
        figmph = px.pie(df_mp_hitung, values='JUMLAH_PAKET', names='METODE_PENGADAAN', title='Grafik Metode Pengadaan - Jumlah Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figmph, theme="streamlit", use_conatiner_width=True)
    with mpn2:
        figmpn = px.pie(df_mp_nilai, values='NILAI_PAKET', names='METODE_PENGADAAN', title='Grafik Metode Pengadaan - Nilai Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figmpn, theme='streamlit', use_container_width=True)

    ##########

    st.markdown("### Jenis Pengadaan")
    jph1, jph2 = st.columns((5,5))
    with jph1:
        st.markdown("#### Berdasarkan Jumlah Paket")
        AgGrid(df_jp_hitung)
    with jph2:
        st.markdown("#### Berdasarkan Nilai Paket")
        AgGrid(df_jp_nilai)

    jpn1, jpn2 = st.columns((5,5))
    with jpn1:
        figjph = px.pie(df_jp_hitung, values='JUMLAH_PAKET', names='JENIS_PENGADAAN', title='Grafik Jenis Pengadaan - Jumlah Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figjph, theme="streamlit", use_conatiner_width=True)
    with jpn2:
        figjpn = px.pie(df_jp_nilai, values='NILAI_PAKET', names='JENIS_PENGADAAN', title='Grafik Jenis Pengadaan - Nilai Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figjpn, theme='streamlit', use_container_width=True)

with tab2:
    # Tab Struktur Anggaran Perangkat Daerah

    ### Tampilan Struktur Anggaran Perangkat Daerah
    st.markdown(f"## **STRUKTUR ANGGARAN - {pilih} - PERANGKAT DAERAH - {tahun}**")

    sql_sa = """
        SELECT nama_satker AS NAMA_SATKER, SUM(belanja_operasi) AS BELANJA_OPERASI, SUM(belanja_modal) AS BELANJA_MODAL, SUM(belanja_pengadaan) AS BELANJA_PENGADAAN, SUM(total_belanja) AS TOTAL_BELANJA 
        FROM df_rsap 
        GROUP BY nama_satker
        ORDER BY total_belanja DESC;
    """
    posisi_sa = con.execute(sql_sa).df()
    AgGrid(posisi_sa)

with tab3:
    # Tab RUP PERANGKAT DAERAH
    st.markdown(f"## **RUP PERANGKAT DAERAH TAHUN {tahun}**")

    ### Tampilan pilihan menu nama opd
    opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='tab3')
    
    rup_pdppsql = con.execute(f"SELECT * FROM df_pp_umumkan WHERE namasatker = '{opd}'").df()
    rup_pdswsql = con.execute(f"SELECT * FROM df_sw_umumkan WHERE namasatker = '{opd}'").df()
    
    belanja_pengadaan_pdsql = con.execute(f"SELECT * FROM df_rsap WHERE nama_satker = '{opd}'").df()
    belanja_operasional_pdsql = con.execute(f"SELECT * FROM df_rsap WHERE nama_satker = '{opd}'").df()
    belanja_modal_pdsql = con.execute(f"SELECT * FROM df_rsap WHERE nama_satker = '{opd}'").df()
    belanja_total_pdsql = con.execute(f"SELECT * FROM df_rsap WHERE nama_satker = '{opd}'").df()

    df_mp_hitung = con.execute(f"SELECT metodepengadaan AS METODE_PENGADAAN, COUNT(metodepengadaan) AS JUMLAH_PAKET FROM rup_pdppsql WHERE metodepengadaan IS NOT NULL GROUP BY metodepengadaan;").df()
    df_mp_nilai = con.execute(f"SELECT metodepengadaan AS METODE_PENGADAAN, SUM(jumlahpagu) AS NILAI_PAKET FROM rup_pdppsql WHERE metodepengadaan IS NOT NULL GROUP BY metodepengadaan;").df()
    df_jp_hitung = con.execute(f"SELECT jenispengadaan AS JENIS_PENGADAAN, COUNT(jenispengadaan) AS JUMLAH_PAKET FROM rup_pdppsql WHERE jenispengadaan IS NOT NULL GROUP BY jenispengadaan").df()
    df_jp_nilai = con.execute(f"SELECT jenispengadaan AS JENIS_PENGADAAN, SUM(jumlahpagu) AS NILAI_PAKET FROM rup_pdppsql WHERE jenispengadaan IS NOT NULL GROUP BY jenispengadaan").df()

    ### Tampilan RUP Perangkat Daerah
    unduh_rupdp = unduh_data(rup_pdppsql)
    unduh_rupsw = unduh_data(rup_pdswsql)

    d1, d2, d3 = st.columns((6,2,2))
    with d1:
        st.markdown(f"### **{opd}**")
    with d2:
        st.download_button(
            label = "📥 Download RUP Penyedia",
            data = unduh_rupdp,
            file_name = f"ruppenyedia-{opd}.csv",
            mime = "text/csv"            
        )
    with d3:
         st.download_button(
            label = "📥 Download RUP Swakelola",
            data = unduh_rupsw,
            file_name = f"rupswakelola-{opd}.csv",
            mime = "text/csv"            
        )       

    ### RUP struktur anggaran
    st.markdown("### Struktur Anggaran")
    belanja_pengadaan_pd = belanja_pengadaan_pdsql['belanja_pengadaan'].sum()
    belanja_pengadaan_pd_print = format_currency(belanja_pengadaan_pd, 'Rp. ', locale='id_ID')

    belanja_operasional_pd = belanja_operasional_pdsql['belanja_operasi'].sum()
    belanja_operasional_pd_print = format_currency(belanja_operasional_pd, 'Rp. ', locale='id_ID')

    belanja_modal_pd = belanja_modal_pdsql['belanja_modal'].sum()
    belanja_modal_pd_print = format_currency(belanja_modal_pd, 'Rp. ', locale='id_ID')

    belanja_total_pd = belanja_total_pdsql['total_belanja'].sum()
    belanja_total_pd_print = format_currency(belanja_total_pd, 'Rp. ', locale='id_ID')

    sa1, sa2, sa3, sa4 = st.columns(4)
    sa1.metric("Belanja Pengadaan", belanja_pengadaan_pd_print)
    sa2.metric("Belanja Operasional", belanja_operasional_pd_print)
    sa3.metric("Belanja Modal", belanja_modal_pd_print)
    sa4.metric("Belanja Total", belanja_total_pd_print)

    ### Posisi input RUP
    st.markdown("### Posisi Input RUP")

    jumlah_total_rup_pd = rup_pdppsql.shape[0] + rup_pdswsql.shape[0]
    nilai_total_rup_pd = rup_pdppsql['jumlahpagu'].sum() + rup_pdswsql['jumlahpagu'].sum()
    nilai_total_rup_pd_print = format_currency(nilai_total_rup_pd, 'Rp. ', locale='id_ID')

    pir1, pir2, pir3 = st.columns(3)
    pir1.metric("", "Jumlah Total")
    pir2.metric("Jumlah Total Paket RUP", jumlah_total_rup_pd)
    pir3.metric("Nilai Total Paket RUP", nilai_total_rup_pd_print)

    jumlah_rup_umumkan_pd = rup_pdppsql.shape[0]
    nilai_rup_umumkan_pd = rup_pdppsql['jumlahpagu'].sum()
    nilai_rup_umumkan_pd_print = format_currency(nilai_rup_umumkan_pd, 'Rp. ', locale='id_ID')

    pirpp1, pirpp2, pirpp3 = st.columns(3)
    pirpp1.metric("","Paket Penyedia")
    pirpp2.metric("Jumlah Total Paket RUP", jumlah_rup_umumkan_pd)
    pirpp3.metric("Nilai Total Paket RUP", nilai_rup_umumkan_pd_print)

    jumlah_rup_sw_umumkan_pd = rup_pdswsql.shape[0]
    nilai_rup_sw_umumkan_pd = rup_pdswsql['jumlahpagu'].sum()
    nilai_rup_sw_umumkan_pd_print = format_currency(nilai_rup_sw_umumkan_pd, 'Rp. ', locale='id_ID')

    pirsw1, pirsw2, pirsw3 = st.columns(3)
    pirsw1.metric("", "Paket Swakelola")
    pirsw2.metric("Jumlah Total Paket RUP", jumlah_rup_sw_umumkan_pd)
    pirsw3.metric("Nilai Total paket RUP", nilai_rup_sw_umumkan_pd_print)

    ### Persentase input RUP
    persen_capaian_rup_pd = (nilai_total_rup_pd / belanja_pengadaan_pd)
    persen_capaian_rup_pd_print = "{:.2%}".format(persen_capaian_rup_pd)

    pr1, pr2, pr3 = st.columns(3)
    pr1.metric("", "")
    pr2.metric("", "Persentase Capaian RUP")
    pr3.metric("Persentase Capaian RUP", persen_capaian_rup_pd_print)

    ### Metode dan Jenis Pengadaan
    st.markdown("### Metode Pengadaan")
    mph1, mph2 = st.columns((5,5))
    with mph1:
        st.markdown("#### Berdasarkan Jumlah Paket")
        AgGrid(df_mp_hitung)
    with mph2:
        st.markdown("#### Berdasarkan Nilai Paket")
        AgGrid(df_mp_nilai)

    mpn1, mpn2 = st.columns((5,5))
    with mpn1:
        figmph = px.pie(df_mp_hitung, values='JUMLAH_PAKET', names='METODE_PENGADAAN', title='Grafik Metode Pengadaan - Jumlah Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figmph, theme="streamlit", use_conatiner_width=True)
    with mpn2:
        figmpn = px.pie(df_mp_nilai, values='NILAI_PAKET', names='METODE_PENGADAAN', title='Grafik Metode Pengadaan - Nilai Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figmpn, theme='streamlit', use_container_width=True)

    ##########

    st.markdown("### Jenis Pengadaan")
    jph1, jph2 = st.columns((5,5))
    with jph1:
        st.markdown("#### Berdasarkan Jumlah Paket")
        AgGrid(df_jp_hitung)
    with jph2:
        st.markdown("#### Berdasarkan Nilai Paket")
        AgGrid(df_jp_nilai)

    jpn1, jpn2 = st.columns((5,5))
    with jpn1:
        figjph = px.pie(df_jp_hitung, values='JUMLAH_PAKET', names='JENIS_PENGADAAN', title='Grafik Jenis Pengadaan - Jumlah Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figjph, theme="streamlit", use_conatiner_width=True)
    with jpn2:
        figjpn = px.pie(df_jp_nilai, values='NILAI_PAKET', names='JENIS_PENGADAAN', title='Grafik Jenis Pengadaan - Nilai Paket', hole=.3, width=800, height=800)
        st.plotly_chart(figjpn, theme='streamlit', use_container_width=True)

with tab4:
    # RUP PAKET PENYEDIA TIAP OPD TABULASI DATA
    st.markdown(f"## **RUP PAKET PENYEDIA TAHUN {tahun}**")

    ### Tampilan pilihan menu nama OPD
    opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='tab4')

    rup_pdppsql = con.execute(f"SELECT * FROM df_pp_umumkan WHERE namasatker = '{opd}'").df()
    rup_pdppsql_tampil = con.execute(f"SELECT idrup AS KODE_RUP, namapaket AS NAMA_PAKET, metodepengadaan AS METODE_PENGADAAN, jenispengadaan AS JENIS_PENGADAAN, statuspdn AS STATUS_PDN, statususahakecil AS STATUS_USAHA_KECIL, jumlahpagu AS JUMLAH_PAGU FROM rup_pdppsql").df()

    ### Tampilan RUP Perangkat Daerah (Data Penyedia)
    unduh_rupdp = unduh_data(rup_pdppsql)

    ddp1, ddp2 = st.columns((8,2))
    with ddp1:
        st.markdown(f"### **{opd}**")
    with ddp2:
        st.download_button(
            label = "📥 Download RUP Paket Penyedia",
            data = unduh_rupdp,
            file_name = f"ruppenyedia-{opd}.csv",
            mime = "text/csv"             
        )
    
    ### Tabulasi data dan pagination AgGrid
    gd = GridOptionsBuilder.from_dataframe(rup_pdppsql_tampil)
    gd.configure_pagination()
    gd.configure_side_bar()
    gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

    gridOptions = gd.build()

    AgGrid(rup_pdppsql_tampil, gridOptions=gridOptions, enable_enterprise_modules=True)

with tab5:
    # RUP PAKET SWAKELOLA TIAP OPD TABULASI DATA
    st.markdown(f"## **RUP PAKET SWAKELOLA TAHUN {tahun}**")

    ### Tampilan pilihan menu nama OPD
    opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='tab5')

    rup_pdswsql = con.execute(f"SELECT * FROM df_sw_umumkan WHERE namasatker = '{opd}'").df()
    rup_pdswsql_tampil = con.execute(f"SELECT idrup AS KODE_RUP, namapaket AS NAMA_PAKET, tipe_swakelola AS TIPE, ppk AS PPK, volume AS VOLUME, jumlahpagu AS NILAI_PAGU FROM rup_pdswsql ").df()

    ### Tampilan RUP Perangkat Daerah (Data Swakelola)
    unduh_rupsw = unduh_data(rup_pdswsql)

    dsw1, dsw2 = st.columns((8,2))
    with dsw1:
        st.markdown(f"### **{opd}**")
    with dsw2:
        st.download_button(
            label = "📥 Download RUP Paket Swakelola",
            data = unduh_rupsw,
            file_name = f"rupswakelola-{opd}.csv",
            mime = "text/csv"       
        )

    ### Tabulasi data dan pagination AgGrid
    gd = GridOptionsBuilder.from_dataframe(rup_pdswsql_tampil)
    gd.configure_pagination()
    gd.configure_side_bar()
    gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

    gridOptions = gd.build()

    AgGrid(rup_pdswsql_tampil, gridOptions=gridOptions, enable_enterprise_modules=True)