import sqlite3
from pathlib import Path

import streamlit as st

from database.db import get_connection
from utils.password import hash_password
from utils.time_utils import get_bd_time


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
# REGISTER PAGE
# =========================================================

def register_page():

    st.subheader("📝 Register")

    fullname = st.text_input(
        "Full Name",
        key="register_fullname"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button(
        "Register",
        key="register_button"
    ):

        # =================================================
        # VALIDATION
        # =================================================

        if not fullname.strip():

            st.warning(
                "Please enter your full name."
            )
            return

        if not email.strip():

            st.warning(
                "Please enter your email."
            )
            return

        if not password:

            st.warning(
                "Please enter your password."
            )
            return

        fullname = fullname.strip()
        email = email.strip().lower()

        hashed_password = hash_password(password)

        # One timestamp for BOTH databases
        created_at = get_bd_time()

        # =================================================
        # 1. SAVE USER TO NEON
        # =================================================

        neon_conn = get_connection()

        try:

            with neon_conn.cursor() as c:

                c.execute(
                    """
                    INSERT INTO users(
                        fullname,
                        email,
                        password,
                        created_at
                    )
                    VALUES(%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        fullname,
                        email,
                        hashed_password,
                        created_at
                    )
                )

                user_id = c.fetchone()[0]

            neon_conn.commit()

        except Exception as e:

            neon_conn.rollback()

            error_message = str(e).lower()

            if (
                "unique" in error_message
                or "duplicate" in error_message
            ):
                st.error(
                    "Email already exists."
                )
            else:
                st.error(
                    f"Registration failed: {e}"
                )

            return

        finally:

            neon_conn.close()

        # =================================================
        # 2. SAVE SAME USER TO SQLITE IMMEDIATELY
        # =================================================

        sqlite_conn = get_sqlite_connection()

        try:

            sqlite_conn.execute(
                """
                INSERT OR REPLACE INTO users(
                    id,
                    fullname,
                    email,
                    password,
                    created_at
                )
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    fullname,
                    email,
                    hashed_password,
                    created_at
                )
            )

            sqlite_conn.commit()

            # =================================================
            # VERIFY SQLITE
            # =================================================

            saved_user = sqlite_conn.execute(
                """
                SELECT
                    id,
                    fullname,
                    email,
                    created_at
                FROM users
                WHERE id = ?
                """,
                (user_id,)
            ).fetchone()

            print(
                "USER SAVED TO SQLITE:",
                saved_user
            )

        except Exception as e:

            sqlite_conn.rollback()

            print(
                "SQLite user sync error:",
                e
            )

            st.warning(
                "Registration successful, "
                "but SQLite synchronization failed."
            )

        finally:

            sqlite_conn.close()

        # =================================================
        # SUCCESS
        # =================================================

        st.success(
            "Registration Successful ✅"
        )