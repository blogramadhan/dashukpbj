import duckdb
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

# Persiapan Dataset
## Dataset ITKP UKPBJ
con = duckdb.connect()
DatasetSIRUPDP = f"data/ITKP/{kodeFolder}/sirupdp{str(tahun)}.parquet"
DatasetSIRUPSW = f"data/ITKP/{kodeFolder}/sirupdsw{str(tahun)}.parquet"
DatasetSIRUPDSARSAP = f"data/ITKP/{kodeFolder}/sirupdsa_rsap{str(tahun)}.parquet"
#DatasetTENDERDTS = f"data/ITKP/{kodeFolder}/dtender_dts{str(tahun)}.parquet"
#DatasetTENDERDTKS = f"data/ITKP/{kodeFolder}/dtender_dtks{str(tahun)}.parquet"
#DatasetNTENDERDNTS = f"data/ITKP/{kodeFolder}/dntender_dnts{str(tahun)}.parquet"
#DatasetKATALOG = f"data/ePurchasing/{kodeFolder}/trxkatalog{str(tahun)}.parquet"
#DatasetDARING = f"data/ePurchasing/{kodeFolder}/daring{str(tahun)}.parquet"

### Query Data RUP paket penyedia
df_pp = pd.read_parquet(DatasetSIRUPDP)
#df_pp_umumkan = df_pp[df_pp['statusumumkan'].isin(['Terumumkan'])]
#df_pp_belum_umumkan = df_pp[df_pp['statusumumkan'].isin(['Draf', 'Draf Lengkap', 'Final Draft'])]
#df_pp_umumkan_umk = df_pp_umumkan[df_pp_umumkan['statususahakecil'] == 'UsahaKecil']
#df_pp_umumkan_pdn = df_pp_umumkan[df_pp_umumkan['statuspdn'] == 'PDN']

#df_pp_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender', 'Tender Cepat', 'Seleksi'])]
#df_pp_tender = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender'])]
#df_pp_tender_cepat = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender Cepat'])]
#df_pp_seleksi = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Seleksi'])]

#df_pp_non_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung', 'Penunjukan Langsung'])]
#df_pp_pengadaan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung'])]
#df_pp_penunjukan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Penunjukan Langsung'])]

#df_pp_epurchasing = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['e-Purchasing'])]


df_pp_umumkan = con.execute("SELECT * FROM df_pp WHERE statusumumkan = 'Terumumkan'").df()
df_pp_belum_umumkan = con.execute("SELECT * FROM df_pp WHERE statusumumkan IN ('Draf','Draf Lengkap','Final Draft')").df()
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
df_sw = pd.read_parquet(DatasetSIRUPSW)
#df_sw_umumkan = df_sw[df_sw['statusumumkan'] == 'Terumumkan']
#df_sw_inisiasi = df_sw[df_sw['statusumumkan'] == 'Terinisiasi']
df_sw_umumkan = con.execute("SELECT * FROM df_sw WHERE statusumumkan = 'Terumumkan'").df()
df_sw_inisiasi = con.execute("SELECT * FROM df_sw WHERE statusumumkan = 'Terinisiasi'").df()

### Data struktur anggaran RUP
df_rsap = pd.read_parquet(DatasetSIRUPDSARSAP)

### Data Tender
#df_dts = pd.read_parquet(DatasetTENDERDTS)
#df_dtks = pd.read_parquet(DatasetTENDERDTKS)

### Data Non Tender
#df_dnts = pd.read_parquet(DatasetNTENDERDNTS)

### Data Katalog
#df_katalog = pd.read_parquet(DatasetKATALOG)

### Data Daring
#df_daring = pd.read_parquet(DatasetDARING)

######### 

# Buat tab ITKP UKPBJ dan ITKP Perangkat Daerah
tab1, tab2 = st.tabs(["RUP KALBAR", "RUP PERANGKAT DAERAH"])

with tab1:
    # Tab pemanfaatan SIRUP

    ### Tampilan pemanfaatan SIRUP
    st.markdown(f"## **RUP KALBAR - {tahun}**")

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

    ### Posisi input RUP
    st.markdown(f"### Posisi Input RUP")
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
    st.markdown(f"## **RUP PERANGKAT DAERAH - {tahun}**")
 
    ### Pengumuman e-Tendering
    st.markdown(f"### Pilih Perangkat Daerah")