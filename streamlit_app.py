import streamlit as st
import pandas as pd
import cx_Oracle

# Fungsi untuk membuat koneksi ke database Oracle
def connect_to_oracle():
    try:
        dsn_tns = cx_Oracle.makedsn('KAF-Tableau.kaf.co.id', '1521', service_name='XE')
        connection = cx_Oracle.connect(user='KAFTABLEAU', password='KAFTABLEAU!', dsn=dsn_tns)
        return connection
    except cx_Oracle.DatabaseError as e:
        st.error(f"Database connection error: {e}")
        return None

# Fungsi untuk mengambil data dari tabel di Oracle
def fetch_data_from_oracle(query):
    conn = connect_to_oracle()
    if conn is None:
        return None
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except cx_Oracle.DatabaseError as e:
        st.error(f"Error fetching data: {e}")
        return None
    finally:
        conn.close()

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

                # Tampilkan data dalam tabel
                st.dataframe(df)
            else:
                st.warning("Tidak ada data yang diambil.")

# Jalankan aplikasi
if __name__ == "__main__":
    main()
