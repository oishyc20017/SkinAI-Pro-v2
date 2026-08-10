from database.db import (
    get_connection,
    get_database_backend
)

from utils.time_utils import get_bd_time


# =========================================================
# PLACEHOLDER
# =========================================================

def _placeholder():

    return (
        "?"
        if get_database_backend() == "sqlite"
        else "%s"
    )


# =========================================================
# SAVE PREDICTION
# =========================================================

def save_prediction(
    user_id,
    disease,
    confidence
):

    conn = get_connection()
    c = conn.cursor()

    p = _placeholder()

    try:

        c.execute(
            f"""
            INSERT INTO prediction_history(
                user_id,
                disease,
                confidence,
                created_at
            )
            VALUES ({p}, {p}, {p}, {p})
            """,
            (
                user_id,
                disease,
                confidence,
                get_bd_time()
            )
        )

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


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

        return c.fetchone()

    finally:

        conn.close()


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

        return c.fetchone()

    finally:

        conn.close()


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
                booking_time,
                status
            FROM bookings
            WHERE user_id={p}
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return c.fetchone()

    finally:

        conn.close()