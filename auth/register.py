import streamlit as st

from database.db import get_connection
from utils.password import hash_password


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
            st.warning("Please fill all fields.")
            return

        conn = get_connection()
        c = conn.cursor()

        try:

            c.execute(
                """
                INSERT INTO users(fullname,email,password)
                VALUES(?,?,?)
                """,
                (
                    fullname,
                    email,
                    hash_password(password)
                )
            )

            conn.commit()

            st.success("Registration Successful ✅")

        except Exception:

            st.error("Email already exists.")

        finally:

            conn.close()