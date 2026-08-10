from database.db import get_connection


# =========================================================
# GET PREDICTION HISTORY
# =========================================================

def get_prediction_history(user_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

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

            return c.fetchall()

    finally:

        conn.close()


# =========================================================
# DELETE PREDICTION
# =========================================================

def delete_prediction(prediction_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

            c.execute(
                """
                DELETE FROM prediction_history
                WHERE id=%s
                """,
                (prediction_id,)
            )

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()