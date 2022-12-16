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

st.title("Dashboard UKPBJ")
st.write("Dashboard ini dibuat untuk menyajikan data ITKP dan transaksi E-Purchasing di Provinsi Kalimantan Barat. \
        Untuk dapat menggunakan dashboard ini, silahkan memilih UKPBJ yang diinginkan di menu sebelah kiri")

# Buat session pilihan UKPBJ
#daerah =    ["PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", 
#            "KAB. BENGKAYANG", "KAB. LANDAK", "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", 
#            "KAB. KAYONG UTARA", "KAB. KETAPANG"]

#if "ukpbj" not in st.session_state:
#    st.session_state["ukpbj"] = ""

#ukpbj = st.sidebar.selectbox("Pilih UKPBJ yang diinginkan :", daerah)

#st.session_state["ukpbj"] = ukpbj