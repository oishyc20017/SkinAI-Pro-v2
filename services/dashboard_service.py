import sqlite3

from database.db import (
    get_connection,
    get_database_backend,
    SQLITE_DB_PATH
)

from utils.time_utils import get_bd_time


# =========================================================
# PLACEHOLDER
# =========================================================

def _placeholder():
    return "?" if get_database_backend() == "sqlite" else "%s"


# =========================================================
# SAVE PREDICTION
# SQLITE + NEON
# =========================================================

def save_prediction(user_id, disease, confidence):

    created_at = get_bd_time()

    # =====================================================
    # 1. SAVE TO SQLITE
    # =====================================================

    sqlite_conn = sqlite3.connect(
        str(SQLITE_DB_PATH)
    )

    try:

        sqlite_conn.execute(
            "PRAGMA foreign_keys = ON"
        )

        sqlite_conn.execute(
            """
            INSERT INTO prediction_history(
                user_id,
                disease,
                confidence,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                disease,
                confidence,
                created_at
            )
        )

        sqlite_conn.commit()

    finally:

        sqlite_conn.close()


    # =====================================================
    # 2. SAVE TO NEON
    # =====================================================

    if get_database_backend() != "neon":

        return


    neon_conn = get_connection()

    try:

        neon_conn.execute(
            """
            INSERT INTO prediction_history(
                user_id,
                disease,
                confidence,
                created_at
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_id,
                disease,
                confidence,
                created_at
            )
        )

        neon_conn.commit()

    finally:

        neon_conn.close()


# =========================================================
# RECENT PREDICTION
# =========================================================

def get_recent_prediction(user_id):

    conn = get_connection()
    c = conn.cursor()

    p = _placeholder()

    try:

        c.execute(
            f"""
            SELECT
                disease,
                confidence
            FROM prediction_history
            WHERE user_id={p}
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        row = c.fetchone()

    finally:

        conn.close()

    return row


# =========================================================
# RECENT CHAT
# =========================================================

def get_recent_chat(user_id):

    conn = get_connection()
    c = conn.cursor()

    p = _placeholder()

    try:

        c.execute(
            f"""
            SELECT
                message
            FROM messages
            WHERE user_id={p}
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        row = c.fetchone()

    finally:

        conn.close()

    return row


# =========================================================
# RECENT BOOKING
# =========================================================

def get_recent_booking(user_id):

    conn = get_connection()
    c = conn.cursor()

    p = _placeholder()

    try:

        c.execute(
            f"""
            SELECT
                doctor_name,
                booking_date,
                booking_time
            FROM bookings
            WHERE user_id={p}
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        row = c.fetchone()

    finally:

        conn.close()

    return row