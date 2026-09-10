import os
import time
import sqlite3
from pathlib import Path

import psycopg
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

SQLITE_DB = BASE_DIR / "skinai.db"

# Neon check interval
SYNC_INTERVAL = 1


# =========================================================
# NEON CONNECTION
# =========================================================

def get_neon_connection():
    """
    Connect to Neon PostgreSQL.

    First tries Windows environment variable.
    If not available, uses Streamlit secrets.

    The database URL is never printed.
    """

    database_url = os.environ.get("NEON_DATABASE_URL")

    if not database_url:
        database_url = st.secrets.get("NEON_DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "NEON_DATABASE_URL is not configured."
        )

    return psycopg.connect(
        database_url,
        connect_timeout=10
    )


# =========================================================
# SQLITE CONNECTION
# =========================================================

def get_sqlite_connection():

    if not SQLITE_DB.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {SQLITE_DB}"
        )

    conn = sqlite3.connect(
        str(SQLITE_DB),
        timeout=30
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# GENERIC TABLE UPSERT
# =========================================================

def upsert_table(
    neon_conn,
    sqlite_conn,
    table_name,
    columns
):
    """
    Copy all rows from Neon into SQLite.

    Existing rows are updated.
    New rows are inserted.
    """

    column_list = ", ".join(columns)

    placeholders = ", ".join(
        ["?" for _ in columns]
    )

    update_columns = [
        column
        for column in columns
        if column != "id"
    ]

    update_clause = ", ".join(
        f"{column}=excluded.{column}"
        for column in update_columns
    )

    sql = f"""
        INSERT INTO {table_name} (
            {column_list}
        )
        VALUES (
            {placeholders}
        )
        ON CONFLICT(id)
        DO UPDATE SET
            {update_clause}
    """

    with neon_conn.cursor() as cursor:

        cursor.execute(
            f"""
            SELECT {column_list}
            FROM {table_name}
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

    for row in rows:

        sqlite_conn.execute(
            sql,
            row
        )

    return len(rows)


# =========================================================
# FIX SQLITE AUTOINCREMENT SEQUENCES
# =========================================================

def fix_sqlite_sequences(sqlite_conn):

    tables = [
        "users",
        "conversations",
        "messages",
        "prediction_history",
        "bookings"
    ]

    for table in tables:

        try:

            max_id = sqlite_conn.execute(
                f"""
                SELECT COALESCE(MAX(id), 0)
                FROM {table}
                """
            ).fetchone()[0]

            sqlite_conn.execute(
                """
                DELETE FROM sqlite_sequence
                WHERE name = ?
                """,
                (table,)
            )

            sqlite_conn.execute(
                """
                INSERT INTO sqlite_sequence(
                    name,
                    seq
                )
                VALUES(
                    ?,
                    ?
                )
                """,
                (
                    table,
                    max_id
                )
            )

        except sqlite3.OperationalError:
            pass


# =========================================================
# ONE COMPLETE SYNC
# =========================================================

def sync_once():

    neon_conn = None
    sqlite_conn = None

    try:

        print()
        print("----------------------------------------")
        print("NEON -> LOCAL SQLITE SYNC")
        print("Checking for updates...")

        # -------------------------------------------------
        # CONNECT TO NEON
        # -------------------------------------------------

        neon_conn = get_neon_connection()

        print("Neon connected successfully.")

        # -------------------------------------------------
        # CONNECT TO SQLITE
        # -------------------------------------------------

        sqlite_conn = get_sqlite_connection()

        print(
            f"SQLite database: {SQLITE_DB}"
        )

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        users = upsert_table(
            neon_conn,
            sqlite_conn,
            "users",
            [
                "id",
                "fullname",
                "email",
                "password",
                "created_at"
            ]
        )

        # -------------------------------------------------
        # CONVERSATIONS
        # -------------------------------------------------

        conversations = upsert_table(
            neon_conn,
            sqlite_conn,
            "conversations",
            [
                "id",
                "user_id",
                "title",
                "created_at"
            ]
        )

        # -------------------------------------------------
        # MESSAGES
        # -------------------------------------------------

        messages = upsert_table(
            neon_conn,
            sqlite_conn,
            "messages",
            [
                "id",
                "conversation_id",
                "user_id",
                "role",
                "message",
                "created_at"
            ]
        )

        # -------------------------------------------------
        # PREDICTION HISTORY
        # -------------------------------------------------

        predictions = upsert_table(
            neon_conn,
            sqlite_conn,
            "prediction_history",
            [
                "id",
                "user_id",
                "disease",
                "confidence",
                "image_path",
                "created_at"
            ]
        )

        # -------------------------------------------------
        # BOOKINGS
        # -------------------------------------------------

        bookings = upsert_table(
            neon_conn,
            sqlite_conn,
            "bookings",
            [
                "id",
                "user_id",
                "doctor_name",
                "specialty",
                "hospital_name",
                "patient_name",
                "patient_email",
                "phone",
                "booking_date",
                "booking_time",
                "symptoms",
                "payment_method",
                "status",
                "created_at"
            ]
        )

        # -------------------------------------------------
        # FIX SQLITE AUTOINCREMENT
        # -------------------------------------------------

        fix_sqlite_sequences(
            sqlite_conn
        )

        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------

        sqlite_conn.commit()

        # -------------------------------------------------
        # SHOW COUNTS
        # -------------------------------------------------

        print(
            f"Users          : {users}"
        )

        print(
            f"Conversations  : {conversations}"
        )

        print(
            f"Messages       : {messages}"
        )

        print(
            f"Predictions    : {predictions}"
        )

        print(
            f"Bookings       : {bookings}"
        )

        print(
            "SQLite updated successfully."
        )

        print("----------------------------------------")

    except Exception as e:

        if sqlite_conn is not None:

            try:
                sqlite_conn.rollback()
            except Exception:
                pass

        print()
        print(
            "SYNC ERROR:",
            repr(e)
        )

        print(
            "The sync process will retry automatically."
        )

    finally:

        if sqlite_conn is not None:
            sqlite_conn.close()

        if neon_conn is not None:
            neon_conn.close()


# =========================================================
# CONTINUOUS SYNC
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("NEON -> SQLITE CONTINUOUS SYNC")
    print("==========================================")

    print(
        f"SQLite database: {SQLITE_DB}"
    )

    print(
        f"Sync interval: {SYNC_INTERVAL} second"
    )

    print(
        "Press CTRL+C to stop."
    )

    print("==========================================")

    while True:

        sync_once()

        time.sleep(
            SYNC_INTERVAL
        )