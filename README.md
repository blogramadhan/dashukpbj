# Dashboard Pengadaan Barang dan Jasa

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
* **ePurchasing**
  * Katalog Lokal
  * Toko Daring
* Indeks Tata Kelola PBJ

*Made with love* dengan menggunakan bahasa programming [Python](https://www.python.org/) dengan beberapa *library* utama seperti:
* [Pandas](https://pandas.pydata.org/)
* [Streamlit](https://streamlit.io)
* [DuckDB](https://duckdb.org)

Sumber data dari *Dashboard* ini berasal dari **API JSON** yang ditarik harian dari [ISB LKPP](https://lkpp.go.id). Data tersebut kemudian disimpan di [Google Cloud Storage](https://google.com) untuk kemudian diolah lebih lanjut dengan [Python](https://python.org).

@2022 - **UlarKadut**  