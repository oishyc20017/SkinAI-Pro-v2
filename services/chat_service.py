import sqlite3
from pathlib import Path

from database.db import get_connection
from utils.time_utils import get_bd_time, format_bd_time


# =========================================================
# LOCAL SQLITE DATABASE
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

def create_conversation(
    user_id,
    title="New Chat"
):

    created_at = get_bd_time()

    # =====================================================
    # 1. SAVE TO NEON
    # =====================================================

    neon_conn = None

    try:

        neon_conn = get_connection()

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

        if neon_conn:
            neon_conn.rollback()

        raise

    finally:

        if neon_conn:
            neon_conn.close()


    # =====================================================
    # 2. SAVE TO LOCAL SQLITE
    #
    # This succeeds when running locally.
    # On Streamlit Cloud, failure is ignored because
    # Neon remains the live database.
    # =====================================================

    try:

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

    except Exception as e:

        print(
            "SQLite conversation sync skipped:",
            e
        )


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

    neon_conn = None

    try:

        neon_conn = get_connection()

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

        if neon_conn:
            neon_conn.rollback()

        raise

    finally:

        if neon_conn:
            neon_conn.close()


    # =====================================================
    # 2. SAVE SAME MESSAGE TO LOCAL SQLITE
    # =====================================================

    try:

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

    except Exception as e:

        print(
            "SQLite message sync skipped:",
            e
        )


# =========================================================
# LOAD MESSAGES
# =========================================================

def load_messages(
    conversation_id
):

    conn = None

    try:

        conn = get_connection()

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
                (
                    conversation_id,
                )
            )

            rows = c.fetchall()

    finally:

        if conn:
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

def load_conversations(
    user_id
):

    conn = None

    try:

        conn = get_connection()

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
                (
                    user_id,
                )
            )

            return c.fetchall()

    finally:

        if conn:
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

    neon_conn = None

    try:

        neon_conn = get_connection()

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

        if neon_conn:
            neon_conn.rollback()

        raise

    finally:

        if neon_conn:
            neon_conn.close()


    # =====================================================
    # 2. UPDATE LOCAL SQLITE
    # =====================================================

    try:

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

    except Exception as e:

        print(
            "SQLite conversation title sync skipped:",
            e
        )