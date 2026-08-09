import psycopg
import streamlit as st

conn = psycopg.connect(
    st.secrets["NEON_DATABASE_URL"]
)

c = conn.cursor()

print("Neon connected successfully")

c.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name
""")

print(c.fetchall())

conn.close()
