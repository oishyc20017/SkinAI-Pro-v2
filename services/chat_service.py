from database.db import get_connection
from utils.time_utils import get_bd_time, format_bd_time


# =========================================================
# CREATE CONVERSATION
# =========================================================

def create_conversation(user_id, title="New Chat"):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            INSERT INTO conversations(
                user_id,
                title,
                created_at
            )
            VALUES(%s, %s, %s)
            RETURNING id
            """,
            (
                user_id,
                title,
                get_bd_time()
            )
        )

        conversation_id = c.fetchone()[0]

        conn.commit()

        return conversation_id

    finally:

        conn.close()


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    conversation_id,
    user_id,
    role,
    message
):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            INSERT INTO messages(
                conversation_id,
                user_id,
                role,
                message,
                created_at
            )
            VALUES(%s, %s, %s, %s, %s)
            """,
            (
                conversation_id,
                user_id,
                role,
                message,
                get_bd_time()
            )
        )

        conn.commit()

    finally:

        conn.close()


# =========================================================
# LOAD MESSAGES
# =========================================================

def load_messages(conversation_id):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            SELECT
                role,
                message,
                created_at
            FROM messages
            WHERE conversation_id=%s
            ORDER BY id
            """,
            (conversation_id,)
        )

        rows = c.fetchall()

    finally:

        conn.close()

    formatted_rows = []

    for role, message, created_at in rows:

        formatted_rows.append(
            (
                role,
                message,
                format_bd_time(created_at)
            )
        )

    return formatted_rows


# =========================================================
# LOAD CONVERSATIONS
# =========================================================

def load_conversations(user_id):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            SELECT
                id,
                title
            FROM conversations
            WHERE user_id=%s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = c.fetchall()

    finally:

        conn.close()

    return rows


# =========================================================
# UPDATE CONVERSATION TITLE
# =========================================================

def update_conversation_title(
    conversation_id,
    title
):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            UPDATE conversations
            SET title=%s
            WHERE id=%s
            """,
            (
                title,
                conversation_id
            )
        )

        conn.commit()

    finally:

        conn.close()