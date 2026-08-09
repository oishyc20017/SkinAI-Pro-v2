import streamlit as st

from database.db import get_connection, get_database_backend
from utils.password import hash_password


def _placeholder():
    return "?" if get_database_backend() == "sqlite" else "%s"


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

        if not fullname or not email or not password:

            st.warning(
                "Please fill all fields."
            )

            return

        conn = get_connection()
        c = conn.cursor()

        p = _placeholder()

        try:

            c.execute(
                f"""
                INSERT INTO users(
                    fullname,
                    email,
                    password
                )
                VALUES({p}, {p}, {p})
                """,
                (
                    fullname,
                    email,
                    hash_password(password)
                )
            )

            conn.commit()

            st.success(
                "Registration Successful ✅"
            )

        except Exception as e:

            conn.rollback()

            # Keep the user-friendly message
            # for duplicate email.
            st.error(
                "Email already exists."
            )

        finally:

            conn.close()