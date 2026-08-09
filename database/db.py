import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

import psycopg
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

    backend = st.secrets.get(
        "DATABASE_BACKEND",
        os.environ.get(
            "DATABASE_BACKEND",
            "sqlite"
        )
    )

    return str(backend).strip().lower()


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    backend = get_database_backend()

    print(
        "DATABASE BACKEND =",
        backend
    )


    # =====================================================
    # LOCAL SQLITE
    # =====================================================

    if backend == "sqlite":

        print(
            "USING SQLITE:",
            SQLITE_DB_PATH
        )

        conn = sqlite3.connect(
            str(SQLITE_DB_PATH),
            check_same_thread=False
        )

        conn.execute(
            "PRAGMA foreign_keys = ON"
        )

        return conn


    # =====================================================
    # NEON POSTGRESQL
    # =====================================================

    if backend == "neon":

        print(
            "USING NEON DATABASE"
        )

        database_url = st.secrets.get(
            "NEON_DATABASE_URL",
            os.environ.get(
                "NEON_DATABASE_URL"
            )
        )

        if not database_url:

            raise RuntimeError(
                "NEON_DATABASE_URL is not configured."
            )

        return psycopg.connect(
            database_url
        )


    # =====================================================
    # INVALID BACKEND
    # =====================================================

    raise RuntimeError(
        f"Unsupported DATABASE_BACKEND: {backend}"
    )