from database.db import get_connection


def get_prediction_history(user_id):

    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            """
            SELECT
                id,
                disease,
                confidence,
                created_at
            FROM prediction_history
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        return c.fetchall()

    finally:
        conn.close()


def delete_prediction(prediction_id):

    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            """
            DELETE FROM prediction_history
            WHERE id=?
            """,
            (prediction_id,)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()