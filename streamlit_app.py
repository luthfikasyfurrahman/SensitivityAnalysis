import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# Fungsi untuk membuat koneksi ke Oracle DB menggunakan SQLAlchemy
def get_oracle_connection():
    try:
        # Format koneksi dengan SQLAlchemy menggunakan cx_Oracle
        engine = create_engine(
            'oracle+cx_oracle://KAFTABLEAU:KAFTABLEAU!@KAF-Tableau.kaf.co.id:1521/XE'
        )
        return engine
    except Exception as e:
        st.error(f"Error saat koneksi: {e}")
        return None

# Fungsi untuk mengambil data dari database
def get_data_from_oracle():
    engine = get_oracle_connection()
    if engine:
        try:
            # Query untuk mengambil data
            query = "SELECT * FROM hasilmodel"  # Ganti dengan query yang sesuai
            # Menggunakan pandas untuk membaca data
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            st.error(f"Error saat mengambil data: {e}")
            return None
    else:
        return None

# Menampilkan data di Streamlit
st.title('Streamlit dengan SQLAlchemy dan Koneksi Oracle DB')

# Ambil data dari database
data = get_data_from_oracle()

if data is not None and not data.empty:
    # Menampilkan data dalam bentuk tabel di Streamlit
    st.write("Data dari Oracle DB:")
    st.dataframe(data)  # Menampilkan data dalam bentuk dataframe
else:
    st.write("Tidak ada data atau gagal menghubungkan ke DB")
