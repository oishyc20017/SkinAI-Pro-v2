import sqlite3
import shutil
from pathlib import Path

import psycopg
import streamlit as st


# =========================================================
# DATABASE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

SQLITE_DB = BASE_DIR / "skinai.db"
BACKUP_DB = BASE_DIR / "skinai_before_sync.db"


# =========================================================
# CHECK SQLITE
# =========================================================

if not SQLITE_DB.exists():
    raise FileNotFoundError(
        f"SQLite database not found: {SQLITE_DB}"
    )


# =========================================================
# BACKUP FIRST
# =========================================================

print("Creating SQLite backup...")

shutil.copy2(
    SQLITE_DB,
    BACKUP_DB
)

print(
    f"Backup created: {BACKUP_DB}"
)


# =========================================================
# CONNECTIONS
# =========================================================

sqlite_conn = sqlite3.connect(
    str(SQLITE_DB)
)

sqlite_conn.execute(
    "PRAGMA foreign_keys = ON"
)

neon_url = st.secrets.get(
    "NEON_DATABASE_URL"
)

if not neon_url:
    sqlite_conn.close()

    raise RuntimeError(
        "NEON_DATABASE_URL is not configured."
    )


print("Connecting to Neon...")

neon_conn = psycopg.connect(
    neon_url
)

print("Neon connected successfully.")


# =========================================================
# TABLES
# =========================================================

tables = [
    "users",
    "conversations",
    "messages",
    "prediction_history",
    "bookings"
]


try:

    # =====================================================
    # SYNC USERS
    # =====================================================

    with neon_conn.cursor() as nc:

        nc.execute(
            """
            SELECT
                id,
                fullname,
                email,
                password,
                created_at
            FROM users
            ORDER BY id
            """
        )

        users = nc.fetchall()


    for row in users:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO users(
                id,
                fullname,
                email,
                password,
                created_at
            )
            VALUES(?, ?, ?, ?, ?)
            """,
            row
        )


    print(
        f"Users synced: {len(users)}"
    )


    # =====================================================
    # CONVERSATIONS
    # =====================================================

    with neon_conn.cursor() as nc:

        nc.execute(
            """
            SELECT
                id,
                user_id,
                title,
                created_at
            FROM conversations
            ORDER BY id
            """
        )

        conversations = nc.fetchall()


    for row in conversations:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO conversations(
                id,
                user_id,
                title,
                created_at
            )
            VALUES(?, ?, ?, ?)
            """,
            row
        )


    print(
        f"Conversations synced: {len(conversations)}"
    )


    # =====================================================
    # MESSAGES
    # =====================================================

    with neon_conn.cursor() as nc:

        nc.execute(
            """
            SELECT
                id,
                conversation_id,
                user_id,
                role,
                message,
                created_at
            FROM messages
            ORDER BY id
            """
        )

        messages = nc.fetchall()


    for row in messages:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO messages(
                id,
                conversation_id,
                user_id,
                role,
                message,
                created_at
            )
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            row
        )


    print(
        f"Messages synced: {len(messages)}"
    )


    # =====================================================
    # PREDICTION HISTORY
    # =====================================================

    with neon_conn.cursor() as nc:

        nc.execute(
            """
            SELECT
                id,
                user_id,
                disease,
                confidence,
                image_path,
                created_at
            FROM prediction_history
            ORDER BY id
            """
        )

        predictions = nc.fetchall()


    for row in predictions:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO prediction_history(
                id,
                user_id,
                disease,
                confidence,
                image_path,
                created_at
            )
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            row
        )


    print(
        f"Predictions synced: {len(predictions)}"
    )


    # =====================================================
    # BOOKINGS
    # =====================================================

    with neon_conn.cursor() as nc:

        nc.execute(
            """
            SELECT
                id,
                user_id,
                doctor_name,
                booking_date,
                booking_time,
                status,
                created_at,
                patient_name,
                patient_email,
                phone,
                specialty,
                hospital_name,
                symptoms,
                payment_method
            FROM bookings
            ORDER BY id
            """
        )

        bookings = nc.fetchall()


    for row in bookings:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO bookings(
                id,
                user_id,
                doctor_name,
                booking_date,
                booking_time,
                status,
                created_at,
                patient_name,
                patient_email,
                phone,
                specialty,
                hospital_name,
                symptoms,
                payment_method
            )
            VALUES(
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            row
        )


    print(
        f"Bookings synced: {len(bookings)}"
    )


    # =====================================================
    # COMMIT SQLITE
    # =====================================================

    sqlite_conn.commit()


    # =====================================================
    # FIX SQLITE AUTOINCREMENT COUNTERS
    # =====================================================

    for table in tables:

        sqlite_conn.execute(
            """
            INSERT OR REPLACE INTO sqlite_sequence(
                name,
                seq
            )
            SELECT
                ?,
                COALESCE(MAX(id), 0)
            FROM """
            + table,
            (table,)
        )


    sqlite_conn.commit()


    # =====================================================
    # FINAL COUNTS
    # =====================================================

    print("\nFinal SQLite counts:")

    for table in tables:

        count = sqlite_conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(
            f"{table}: {count}"
        )


    print(
        "\nNeon → SQLite sync completed successfully."
    )


finally:

    sqlite_conn.close()
    neon_conn.close()