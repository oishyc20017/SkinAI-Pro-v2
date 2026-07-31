import streamlit as st
from requests_oauthlib import OAuth2Session

from database.db import get_connection
from utils.password import verify_password
from components.theme import page_title


# =========================================================
# GOOGLE OAUTH CONFIGURATION
# =========================================================

GOOGLE_AUTHORIZATION_ENDPOINT = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_ENDPOINT = (
    "https://oauth2.googleapis.com/token"
)

GOOGLE_USERINFO_ENDPOINT = (
    "https://www.googleapis.com/oauth2/v2/userinfo"
)

GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile"
]


# =========================================================
# GOOGLE LOGIN
# =========================================================

def google_login():

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    redirect_uri = st.secrets["REDIRECT_URI"]

    oauth = OAuth2Session(
        client_id=client_id,
        scope=GOOGLE_SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = oauth.authorization_url(
        GOOGLE_AUTHORIZATION_ENDPOINT,
        access_type="offline",
        prompt="select_account"
    )

    # State is already included in Google's URL.
    # Do NOT depend on Streamlit session_state here.
    st.link_button(
        "🔵 Continue with Google",
        authorization_url,
        use_container_width=True
    )

# =========================================================
# GOOGLE CALLBACK
# =========================================================

def google_callback():

    if "code" not in st.query_params:
        return False

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["REDIRECT_URI"]

    # Get the state returned by Google
    returned_state = st.query_params.get("state")

    if not returned_state:
        st.error(
            "Google OAuth state is missing. Please try again."
        )
        return False

    oauth = OAuth2Session(
        client_id=client_id,
        state=returned_state,
        redirect_uri=redirect_uri
    )

    try:

        code = st.query_params.get("code")

        token = oauth.fetch_token(
            GOOGLE_TOKEN_ENDPOINT,
            code=code,
            client_secret=client_secret
        )

        response = oauth.get(
            GOOGLE_USERINFO_ENDPOINT
        )

        response.raise_for_status()

        user_info = response.json()

        email = user_info.get("email")
        fullname = user_info.get(
            "name",
            "Google User"
        )

        if not email:
            st.error(
                "Google did not return an email address."
            )
            return False

        # ================================================
        # FIND / CREATE USER
        # ================================================

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            SELECT id, fullname, email
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        user = c.fetchone()

        if user is None:

            c.execute(
                """
                INSERT INTO users(
                    fullname,
                    email,
                    password
                )
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
                """
                SELECT id, fullname, email
                FROM users
                WHERE email=?
                """,
                (email,)
            )

            user = c.fetchone()

        conn.close()

        # ================================================
        # LOGIN SESSION
        # ================================================

        st.session_state.logged_in = True
        st.session_state.user_id = user[0]
        st.session_state.fullname = user[1]
        st.session_state.email = user[2]

        # Remove OAuth parameters from URL
        st.query_params.clear()

        return True

    except Exception as e:

        st.error(
            f"Google login failed: {e}"
        )

        return False

# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    # =====================================================
    # CHECK GOOGLE CALLBACK FIRST
    # =====================================================

    if google_callback():

        st.success(
            "Google Login Successful ✅"
        )

        st.rerun()

    # =====================================================
    # PAGE TITLE
    # =====================================================

    page_title("🔐 Login")

    # =====================================================
    # EMAIL LOGIN
    # =====================================================

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
            SELECT id, fullname, email, password
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        user = c.fetchone()

        conn.close()

        if user is None:

            st.error(
                "User not found."
            )

            return

        if verify_password(
            password,
            user[3]
        ):

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.fullname = user[1]
            st.session_state.email = user[2]

            st.success(
                "Login Successful ✅"
            )

            st.rerun()

        else:

            st.error(
                "Incorrect Password."
            )

    # =====================================================
    # SOCIAL LOGIN
    # =====================================================

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

    # =====================================================
    # GOOGLE LOGIN
    # =====================================================

    google_login()

    # =====================================================
    # FACEBOOK LOGIN
    # =====================================================

    if st.button(
        "📘  Continue with Facebook",
        use_container_width=True,
        key="facebook_login_button"
    ):

        st.info(
            "Facebook Login will be connected next."
        )