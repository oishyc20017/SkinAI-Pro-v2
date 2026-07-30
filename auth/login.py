import streamlit as st
import requests
from requests_oauthlib import OAuth2Session
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"

GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"

GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile"
]

from database.db import get_connection
from utils.password import verify_password
from components.theme import page_title
def google_login():

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    redirect_uri = st.secrets["REDIRECT_URI"]

    oauth = OAuth2Session(
        client_id,
        scope=GOOGLE_SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = oauth.authorization_url(
        GOOGLE_AUTHORIZATION_ENDPOINT
    )
    st.write(authorization_url)

    st.session_state.google_oauth_state = state

    st.markdown(
        f'<meta http-equiv="refresh" content="0; url={authorization_url}">',
        unsafe_allow_html=True
    )


def google_callback():

    if "code" not in st.query_params:
        return False

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["REDIRECT_URI"]

    oauth = OAuth2Session(
        client_id,
        state=st.session_state.get("google_oauth_state"),
        redirect_uri=redirect_uri
    )

    token = oauth.fetch_token(
        GOOGLE_TOKEN_ENDPOINT,
        code=st.query_params["code"],
        client_secret=client_secret
    )

    user_info = oauth.get(
        GOOGLE_USERINFO_ENDPOINT
    ).json()

    email = user_info.get("email")
    fullname = user_info.get("name", "Google User")

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT id, fullname, email FROM users WHERE email=?",
        (email,)
    )

    user = c.fetchone()

    if user is None:

        # Temporary password for OAuth-created account
        c.execute(
            """
            INSERT INTO users(fullname,email,password)
            VALUES(?,?,?)
            """,
            (
                fullname,
                email,
                "GOOGLE_OAUTH_USER"
            )
        )

        conn.commit()

        c.execute(
            "SELECT id, fullname, email FROM users WHERE email=?",
            (email,)
        )

        user = c.fetchone()

    conn.close()

    st.session_state.logged_in = True
    st.session_state.user_id = user[0]
    st.session_state.fullname = user[1]
    st.session_state.email = user[2]

    st.query_params.clear()

    return True


def login_page():
    if google_callback():

        st.success("Google Login Successful ✅")
        st.rerun()

    page_title("🔐 Login")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        key="login_button",
        use_container_width=True
    ):

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            SELECT id,fullname,email,password
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        user = c.fetchone()

        conn.close()

        if user is None:

            st.error("User not found.")
            return

        if verify_password(password, user[3]):

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.fullname = user[1]
            st.session_state.email = user[2]

            st.success("Login Successful ✅")
            st.rerun()

        else:

            st.error("Incorrect Password.")

    # =====================================
    # SOCIAL LOGIN
    # =====================================

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#94A3B8;
            font-size:13px;
            margin-bottom:12px;
        ">
            Or continue with
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔵  Continue with Google",
        use_container_width=True,
        key="google_login_button"
    ):

        google_login()

    if st.button(
        "📘  Continue with Facebook",
        use_container_width=True,
        key="facebook_login_button"
    ):

        st.info(
            "Facebook Login will be connected next."
        )