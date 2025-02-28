import streamlit as st
import pandas as pd
import cx_Oracle
from datetime import datetime

# Fungsi untuk membuat koneksi ke database Oracle
def connect_to_oracle():
    try:
        dsn_tns = cx_Oracle.makedsn('KAF-Tableau.kaf.co.id', '1521', service_name='XE')
        connection = cx_Oracle.connect(user='KAFTABLEAU', password='KAFTABLEAU!', dsn=dsn_tns)
        return connection
    except cx_Oracle.DatabaseError as e:
        st.error(f"Database connection error: {e}")
        return None

# Fungsi untuk mengambil daftar komoditas dari database
def get_commodities():
    conn = connect_to_oracle()
    if conn is None:
        return []
    
    try:
        query = "SELECT DISTINCT commodity FROM RM_COMMODITY_PRICE"
        df = pd.read_sql(query, conn)
        return df['COMMODITY'].tolist()
    except cx_Oracle.DatabaseError as e:
        st.error(f"Error fetching commodities: {e}")
        return []
    finally:
        conn.close()

# Fungsi untuk mengambil daftar tanggal dari database
def get_date():
    conn = connect_to_oracle()
    if conn is None:
        return []
    
    try:
        query = "SELECT DISTINCT RECORD_DATE FROM RM_COMMODITY_PRICE ORDER BY RECORD_DATE"
        df = pd.read_sql(query, conn)
        return df['RECORD_DATE'].astype(str).tolist()  # Pastikan tanggal dalam format string
    except cx_Oracle.DatabaseError as e:
        st.error(f"Error fetching Date: {e}")
        return []
    finally:
        conn.close()

# Fungsi untuk mengambil data dari tabel berdasarkan kriteria yang dimasukkan
def fetch_data(x1, x2, x3, date_awal, date_akhir):
    conn = connect_to_oracle()
    if conn is None:
        return None

    try:
        query = f"""
            SELECT record_date, 
                   MAX(CASE WHEN commodity = '{x1}' THEN value END) AS {x1},
                   MAX(CASE WHEN commodity = '{x2}' THEN value END) AS {x2},
                   MAX(CASE WHEN commodity = '{x3}' THEN value END) AS {x3}
            FROM RM_COMMODITY_PRICE
            WHERE record_date BETWEEN TO_DATE('{date_awal}', 'YYYY-MM-DD') 
                                  AND TO_DATE('{date_akhir}', 'YYYY-MM-DD')
            GROUP BY record_date
            ORDER BY record_date
        """
        # Eksekusi query
        df = pd.read_sql(query, conn)
        return df

    except cx_Oracle.DatabaseError as e:
        st.error(f"Error fetching data: {e}")
        return None
    finally:
        conn.close()
        
# Fungsi utama Streamlit
def main():
    st.title("Sensitif Analysis")

    # Memilih Komoditas
    commodities = get_commodities()
    x1 = st.selectbox("Commodity x1:", commodities)
    x2 = st.selectbox("Commodity x2:", commodities)
    x3 = st.selectbox("Commodity x3:", commodities)

    # Memilih tanggal
    date = get_date()
    date_awal = st.selectbox("Date Awal (YYYY-MM-DD):", date)
    date_akhir = st.selectbox("Date Akhir (YYYY-MM-DD):", date)
