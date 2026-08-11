import os
from datetime import datetime, timezone, timedelta

import psycopg
import streamlit as st


# =========================================================
# BANGLADESH TIMEZONE
# =========================================================

BD_TIMEZONE = timezone(timedelta(hours=6))


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
    """
    Neon PostgreSQL is the single live database
    for both Local and Streamlit.
    """

    return "neon"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    database_url = st.secrets.get(
        "NEON_DATABASE_URL",
        os.environ.get("NEON_DATABASE_URL")
    )

    if not database_url:
        raise RuntimeError(
            "NEON_DATABASE_URL is not configured."
        )

    return psycopg.connect(database_url)