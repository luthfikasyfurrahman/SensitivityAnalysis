import streamlit as st
import cx_Oracle
import pandas as pd

# Konek ke DB
def connect_to_oracle():
    try:
        dsn_tns = cx_Oracle.makedsn('KAF-Tableau.kaf.co.id', '1521', service_name='XE')
        connection = cx_Oracle.connect(user='KAFTABLEAU', password='KAFTABLEAU!', dsn=dsn_tns)
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None
    
# Ambil Value Commodity
def get_commodities():
    conn = connect_to_oracle()
    if conn is None:
        return []
    try:
        query = "SELECT DISTINCT commodity FROM RM_COMMODITY_PRICE"
        df = pd.read_sql(query, conn)
        return df['COMMODITY'].tolist()
    except cx_Oracle.DatabaseError as e:
        print(f"Error fetching commodities: {e}")
        return []
    finally:
        conn.close()

# Ambil data dari DB
commodities = get_commodities()

# Menampilkan inputan dropdown untuk x1 dan x2
x1 = st.selectbox("Pilih Commodity untuk x1:", commodities)
x2 = st.selectbox("Pilih Commodity untuk x2:", commodities)

# Fungsi untuk menampilkan output ketika tombol diklik
def tampilkan_output():
    # Menampilkan output berdasarkan x1 dan x2
    st.write(f"Output: x1 = {x1}, x2 = {x2}")

# Tombol untuk memicu output
if st.button("Tampilkan Output"):
    tampilkan_output()
