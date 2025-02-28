import streamlit as st
import cx_Oracle

# Fungsi untuk koneksi ke Oracle DB
def get_oracle_connection():
    try:
        # Masukkan konfigurasi koneksi sesuai dengan database Anda
        conn = cx_Oracle.connect(
            user="your_username",          # Ganti dengan username Anda
            password="your_password",      # Ganti dengan password Anda
            dsn="hostname:port/service_name"  # Ganti dengan hostname, port, dan service name DB
        )
        return conn
    except cx_Oracle.DatabaseError as e:
        st.error(f"Error: {str(e)}")
        return None

# Fungsi untuk mengambil data dari database
def get_data_from_oracle():
    conn = get_oracle_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")  # Ganti dengan query Anda
        data = cursor.fetchall()  # Mengambil semua data
        cursor.close()
        conn.close()
        return data
    else:
        return []

# Menampilkan data di Streamlit
st.title('Streamlit dengan Koneksi Oracle DB')

data = get_data_from_oracle()

if data:
    # Menampilkan data dalam bentuk tabel di Streamlit
    st.write("Data dari Oracle DB:")
    st.write(data)
else:
    st.write("Tidak ada data atau gagal menghubungkan ke DB")
