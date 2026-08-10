import sqlite3
from pathlib import Path

from database.db import get_connection
from utils.time_utils import get_bd_time


# =========================================================
# SQLITE DATABASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "skinai.db"


def get_sqlite_connection():

    conn = sqlite3.connect(
        str(SQLITE_DB_PATH),
        check_same_thread=False
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# SAVE PREDICTION
# =========================================================

def save_prediction(
    user_id,
    disease,
    confidence
):

    created_at = get_bd_time()

    # =====================================================
    # 1. SAVE TO NEON
    # =====================================================

    neon_conn = get_connection()

    try:

        with neon_conn.cursor() as c:

            c.execute(
                """
                INSERT INTO prediction_history(
                    user_id,
                    disease,
                    confidence,
                    created_at
                )
                VALUES(%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    disease,
                    confidence,
                    created_at
                )
            )

            prediction_id = c.fetchone()[0]

        neon_conn.commit()

    except Exception:

        neon_conn.rollback()
        raise

    finally:

        neon_conn.close()


    # =====================================================
    # 2. SAVE SAME PREDICTION TO SQLITE IMMEDIATELY
    # =====================================================

    sqlite_conn = get_sqlite_connection()

    try:

        sqlite_conn.execute(
            """
            INSERT OR IGNORE INTO prediction_history(
                id,
                user_id,
                disease,
                confidence,
                created_at
            )
            VALUES(?, ?, ?, ?, ?)
            """,
            (
                prediction_id,
                user_id,
                disease,
                confidence,
                created_at
            )
        )

        sqlite_conn.commit()

    except Exception as e:

        sqlite_conn.rollback()

        # Neon already contains the prediction.
        # Backup sync will recover SQLite if needed.
        print(
            "SQLite prediction sync error:",
            e
        )

    finally:

        sqlite_conn.close()


# =========================================================
# RECENT PREDICTION
# =========================================================

def get_recent_prediction(user_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

            c.execute(
                """
                SELECT
                    disease,
                    confidence
                FROM prediction_history
                WHERE user_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,)
            )

            return c.fetchone()

    finally:

        conn.close()


# =========================================================
# RECENT CHAT
# =========================================================

def get_recent_chat(user_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

            c.execute(
                """
                SELECT
                    message
                FROM messages
                WHERE user_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,)
            )

            return c.fetchone()

    finally:

        conn.close()


# =========================================================
# RECENT BOOKING
# =========================================================

def get_recent_booking(user_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

            c.execute(
                """
                SELECT
                    doctor_name,
                    booking_date,
                    booking_time,
                    status
                FROM bookings
                WHERE user_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,)
            )

            return c.fetchone()

    finally:

        conn.close()