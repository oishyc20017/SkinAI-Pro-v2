import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
import streamlit as st


# =========================================================
# BANGLADESH TIMEZONE
# =========================================================

BD_TIMEZONE = timezone(timedelta(hours=6))


# =========================================================
# SQLITE DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE_DB_PATH = BASE_DIR / "skinai.db"


# =========================================================
# BANGLADESH CURRENT TIME
# =========================================================

def get_bd_time():
    return datetime.now(BD_TIMEZONE).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =========================================================
# DATABASE BACKEND
# =========================================================

def get_database_backend():
    # আমরা শুধু SQLite ব্যবহার করব
    return "sqlite"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    print("DATABASE BACKEND = sqlite")
    print("USING SQLITE:", SQLITE_DB_PATH)

    conn = sqlite3.connect(
        str(SQLITE_DB_PATH),
        check_same_thread=False
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn