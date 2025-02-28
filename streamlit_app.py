import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Fungsi untuk membuat koneksi ke database Oracle menggunakan SQLAlchemy
def connect_to_oracle():
    try:
        engine = create_engine('oracle+oracledb://KAFTABLEAU:KAFTABLEAU!@KAF-Tableau.kaf.co.id:1521/XE')
        return engine
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Fungsi untuk mengambil data dari tabel di Oracle
def fetch_data_from_oracle(query):
    engine = connect_to_oracle()
    if engine is None:
        return None
    
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Fungsi utama Streamlit
def main():
    st.title("Koneksi ke Oracle Database")

    # Input untuk query SQL
    query = st.text_area("Masukkan query SQL:", "SELECT * FROM RM_COMMODITY_PRICE WHERE ROWNUM <= 10")

    if st.button("Ambil Data"):
        if query:
            df = fetch_data_from_oracle(query)
            if df is not None:
                st.write("Data yang diambil:")
                st.dataframe(df)
            else:
                st.warning("Tidak ada data yang diambil.")

# Jalankan aplikasi
if __name__ == "__main__":
    main()
