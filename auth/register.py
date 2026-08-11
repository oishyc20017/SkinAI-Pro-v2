import sqlite3
from pathlib import Path

import psycopg
import streamlit as st

from database.db import get_connection
from utils.password import hash_password


# =========================================================
# LOCAL SQLITE DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "skinai.db"


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
            st.warning("Please enter your full name.")
            return

        if not email.strip():
            st.warning("Please enter your email.")
            return

        if not password:
            st.warning("Please enter your password.")
            return

        fullname = fullname.strip()
        email = email.strip().lower()

        hashed_password = hash_password(password)

        # =================================================
        # 1. SAVE USER TO NEON
        # =================================================

        neon_conn = None
        user_id = None
        created_at = None

        try:

            neon_conn = get_connection()

            with neon_conn.cursor() as c:

                c.execute(
                    """
                    INSERT INTO users(
                        fullname,
                        email,
                        password,
                        created_at
                    )
                    VALUES(
                        %s,
                        %s,
                        %s,
                        CURRENT_TIMESTAMP
                    )
                    RETURNING id, created_at
                    """,
                    (
                        fullname,
                        email,
                        hashed_password
                    )
                )

                result = c.fetchone()

                user_id = result[0]
                created_at = result[1]

            neon_conn.commit()

        except psycopg.errors.UniqueViolation:

            if neon_conn:
                neon_conn.rollback()

            st.error(
                "Email already exists. Please use another email."
            )

            return

        except Exception as e:

            if neon_conn:
                neon_conn.rollback()

            st.error(
                f"Registration failed: {e}"
            )

            print(
                "Neon registration error:",
                e
            )

            return

        finally:

            if neon_conn:
                neon_conn.close()

        # =================================================
        # 2. SAVE SAME USER TO LOCAL SQLITE
        #
        # This works when the application is running
        # on your own PC.
        # =================================================

        sqlite_conn = None

        try:

            sqlite_conn = sqlite3.connect(
                str(SQLITE_DB_PATH),
                check_same_thread=False
            )

            sqlite_conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            # Convert Neon timestamp to text if necessary
            if created_at is not None:
                created_at_text = str(created_at)
            else:
                created_at_text = None

            sqlite_conn.execute(
                """
                INSERT OR REPLACE INTO users(
                    id,
                    fullname,
                    email,
                    password,
                    created_at
                )
                VALUES(
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    fullname,
                    email,
                    hashed_password,
                    created_at_text
                )
            )

            sqlite_conn.commit()

            print(
                f"USER SAVED TO SQLITE: {user_id}"
            )

        except Exception as e:

            if sqlite_conn:
                sqlite_conn.rollback()

            print(
                "SQLite user sync error:",
                e
            )

            # Neon registration was already successful.
            st.warning(
                "Registration successful, "
                "but local SQLite could not be updated."
            )

        finally:

            if sqlite_conn:
                sqlite_conn.close()

        # =================================================
        # 3. SUCCESS
        # =================================================

        st.success(
            "Registration Successful ✅"
        )

        print(
            f"USER REGISTERED SUCCESSFULLY: "
            f"id={user_id}, email={email}"
        )