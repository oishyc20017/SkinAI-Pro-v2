from database.db import get_connection


def get_prediction_history(user_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT
            id,
            disease,
            confidence,
            created_at
        FROM prediction_history
        WHERE user_id=%s
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = c.fetchall()

    conn.close()

    return rows


def delete_prediction(prediction_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        DELETE FROM prediction_history
        WHERE id=%s
        """,
        (prediction_id,)
    )

    conn.commit()
    conn.close()