import sqlite3
from pathlib import Path

import psycopg
import streamlit as st


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

SQLITE_DB = BASE_DIR / "skinai.db"


# =========================================================
# NEON CONNECTION
# =========================================================

def get_neon_connection():

    neon_url = st.secrets.get("NEON_DATABASE_URL")

    if not neon_url:
        raise RuntimeError(
            "NEON_DATABASE_URL is not configured."
        )

    return psycopg.connect(neon_url)


# =========================================================
# SQLITE CONNECTION
# =========================================================

def get_sqlite_connection():

    if not SQLITE_DB.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {SQLITE_DB}"
        )

    conn = sqlite3.connect(str(SQLITE_DB))

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# SYNC TABLE
# =========================================================

def sync_table(
    neon_conn,
    sqlite_conn,
    table_name,
    columns
):

    column_list = ", ".join(columns)

    placeholders = ", ".join(
        ["?" for _ in columns]
    )

    # -----------------------------------------------------
    # GET DATA FROM NEON
    # -----------------------------------------------------

    with neon_conn.cursor() as cursor:

        cursor.execute(
            f"""
            SELECT {column_list}
            FROM {table_name}
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

    # -----------------------------------------------------
    # INSERT / UPDATE SQLITE
    # -----------------------------------------------------

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
        INSERT INTO {table_name}(
            {column_list}
        )
        VALUES(
            {placeholders}
        )
        ON CONFLICT(id)
        DO UPDATE SET
            {update_clause}
    """

    for row in rows:

        sqlite_conn.execute(
            sql,
            row
        )

    print(
        f"{table_name}: {len(rows)} rows synced"
    )


# =========================================================
# MAIN SYNC
# =========================================================

def sync_neon_to_sqlite():

    print("=" * 60)
    print("NEON → SQLITE SYNC STARTED")
    print("=" * 60)

    neon_conn = None
    sqlite_conn = None

    try:

        # -------------------------------------------------
        # CONNECTIONS
        # -------------------------------------------------

        print("Connecting to Neon...")

        neon_conn = get_neon_connection()

        print("Neon connected successfully.")

        sqlite_conn = get_sqlite_connection()

        print(
            f"Using SQLite: {SQLITE_DB}"
        )

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        sync_table(
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

        sync_table(
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

        sync_table(
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
        # PREDICTIONS
        # -------------------------------------------------

        sync_table(
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

        sync_table(
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
        # COMMIT
        # -------------------------------------------------

        sqlite_conn.commit()

        print()
        print("=" * 60)
        print("SYNC COMPLETED SUCCESSFULLY")
        print("=" * 60)

        # -------------------------------------------------
        # COUNTS
        # -------------------------------------------------

        tables = [
            "users",
            "conversations",
            "messages",
            "prediction_history",
            "bookings"
        ]

        print()
        print("SQLite counts:")

        for table in tables:

            count = sqlite_conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(
                f"{table}: {count}"
            )

    except Exception:

        if sqlite_conn is not None:

            try:
                sqlite_conn.rollback()
            except Exception:
                pass

        raise

    finally:

        if sqlite_conn is not None:
            sqlite_conn.close()

        if neon_conn is not None:
            neon_conn.close()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    sync_neon_to_sqlite()