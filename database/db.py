import os
from datetime import datetime, timezone, timedelta

import psycopg
import streamlit as st


BD_TIMEZONE = timezone(timedelta(hours=6))


def get_bd_time():
    """
    Returns current Bangladesh local time.
    """
    return datetime.now(BD_TIMEZONE).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def get_connection():
    """
    Connect to the shared Neon PostgreSQL database.
    """

    database_url = st.secrets.get(
        "NEON_DATABASE_URL",
        os.environ.get("NEON_DATABASE_URL")
    )

    if not database_url:
        raise RuntimeError(
            "NEON_DATABASE_URL is not configured."
        )

    return psycopg.connect(database_url)