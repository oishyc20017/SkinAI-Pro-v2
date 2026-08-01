from database.db import get_connection
from utils.time_utils import get_bd_time


# =====================================================
# SAVE PREDICTION
# =====================================================

def save_prediction(user_id, disease, confidence):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
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
            get_bd_time()
        )
    )

    conn.commit()
    conn.close()


# =====================================================
# RECENT PREDICTION
# =====================================================

def get_recent_prediction(user_id):

    conn = get_connection()
    c = conn.cursor()

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

    row = c.fetchone()

    conn.close()

    return row


# =====================================================
# RECENT CHAT
# =====================================================

def get_recent_chat(user_id):

    conn = get_connection()
    c = conn.cursor()

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

    row = c.fetchone()

    conn.close()

    return row


# =====================================================
# RECENT BOOKING
# =====================================================

def get_recent_booking(user_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT
            doctor_name,
            booking_date,
            booking_time
        FROM bookings
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = c.fetchone()

    conn.close()

    return row