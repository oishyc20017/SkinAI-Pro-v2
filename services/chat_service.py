from database.db import get_connection
from utils.time_utils import get_bd_time, format_bd_time


def create_conversation(user_id, title="New Chat"):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO conversations(
            user_id,
            title,
            created_at
        )
        VALUES(?,?,?)
        """,
        (
            user_id,
            title,
            get_bd_time()
        )
    )

    conversation_id = c.lastrowid

    conn.commit()
    conn.close()

    return conversation_id


def save_message(
    conversation_id,
    user_id,
    role,
    message
):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO messages(
            conversation_id,
            user_id,
            role,
            message,
            created_at
        )
        VALUES(?,?,?,?,?)
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
    conn.close()


def load_messages(conversation_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT
            role,
            message,
            created_at
        FROM messages
        WHERE conversation_id=?
        ORDER BY id
        """,
        (conversation_id,)
    )

    rows = c.fetchall()

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


def load_conversations(user_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT
            id,
            title
        FROM conversations
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = c.fetchall()

    conn.close()

    return rows


def update_conversation_title(
    conversation_id,
    title
):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        UPDATE conversations
        SET title=?
        WHERE id=?
        """,
        (
            title,
            conversation_id
        )
    )

    conn.commit()
    conn.close()