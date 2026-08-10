import sqlite3
from pathlib import Path

from database.db import get_connection
from utils.time_utils import get_bd_time, format_bd_time


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
# CREATE CONVERSATION
# =========================================================

def create_conversation(user_id, title="New Chat"):

    created_at = get_bd_time()

    # =====================================================
    # 1. SAVE TO NEON
    # =====================================================

    neon_conn = get_connection()

    try:

        with neon_conn.cursor() as c:

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
                    created_at
                )
            )

            conversation_id = c.fetchone()[0]

        neon_conn.commit()

    except Exception:

        neon_conn.rollback()
        raise

    finally:

        neon_conn.close()


    # =====================================================
    # 2. SAVE SAME CONVERSATION TO SQLITE
    # =====================================================

    sqlite_conn = get_sqlite_connection()

    try:

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
            (
                conversation_id,
                user_id,
                title,
                created_at
            )
        )

        sqlite_conn.commit()

    finally:

        sqlite_conn.close()


    return conversation_id


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    conversation_id,
    user_id,
    role,
    message
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
                INSERT INTO messages(
                    conversation_id,
                    user_id,
                    role,
                    message,
                    created_at
                )
                VALUES(%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    conversation_id,
                    user_id,
                    role,
                    message,
                    created_at
                )
            )

            message_id = c.fetchone()[0]

        neon_conn.commit()

    except Exception:

        neon_conn.rollback()
        raise

    finally:

        neon_conn.close()


    # =====================================================
    # 2. SAVE SAME MESSAGE TO SQLITE
    # =====================================================

    sqlite_conn = get_sqlite_connection()

    try:

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
            (
                message_id,
                conversation_id,
                user_id,
                role,
                message,
                created_at
            )
        )

        sqlite_conn.commit()

    finally:

        sqlite_conn.close()


# =========================================================
# LOAD MESSAGES
# =========================================================

def load_messages(conversation_id):

    conn = get_connection()

    try:

        with conn.cursor() as c:

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

    try:

        with conn.cursor() as c:

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

            return c.fetchall()

    finally:

        conn.close()


# =========================================================
# UPDATE CONVERSATION TITLE
# =========================================================

def update_conversation_title(
    conversation_id,
    title
):

    # =====================================================
    # 1. UPDATE NEON
    # =====================================================

    neon_conn = get_connection()

    try:

        with neon_conn.cursor() as c:

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

        neon_conn.commit()

    except Exception:

        neon_conn.rollback()
        raise

    finally:

        neon_conn.close()


    # =====================================================
    # 2. UPDATE SQLITE
    # =====================================================

    sqlite_conn = get_sqlite_connection()

    try:

        sqlite_conn.execute(
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

        sqlite_conn.commit()

    finally:

        sqlite_conn.close()