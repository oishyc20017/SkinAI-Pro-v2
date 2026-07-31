import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent

# Local and Streamlit Cloud use separate databases
environment = st.secrets.get("ENVIRONMENT", "local")

if environment == "cloud":
    DB_PATH = BASE_DIR / "cloud_skinai.db"
else:
    DB_PATH = BASE_DIR / "skinai.db"


BD_TIMEZONE = timezone(timedelta(hours=6))


def get_bd_time():
    """
    Returns current Bangladesh local time.
    """
    return datetime.now(BD_TIMEZONE).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )
    return conn