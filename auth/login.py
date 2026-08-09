import streamlit as st
from requests_oauthlib import OAuth2Session

from database.db import get_connection
from utils.password import verify_password
from components.theme import page_title
from database.db import get_connection, get_database_backend


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
# LOGIN ANIMATION / STYLE
# =========================================================

def login_animation_css():

    st.markdown(
        """
        <style>

        /* =========================================
           MAIN LOGIN AREA
        ========================================= */

        .login-hero {
            position: relative;
            text-align: center;
            padding: 28px 20px 12px 20px;
            overflow: hidden;
        }


        /* =========================================
           ANIMATED AI ORBS
        ========================================= */

        .ai-orb {
            position: absolute;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            filter: blur(35px);
            opacity: 0.35;
            animation: floatOrb 6s ease-in-out infinite;
            pointer-events: none;
        }

        .orb-one {
            background: #38bdf8;
            top: 10px;
            left: 12%;
        }

        .orb-two {
            background: #8b5cf6;
            top: 70px;
            right: 12%;
            animation-delay: 2s;
        }

        @keyframes floatOrb {

            0%, 100% {
                transform: translateY(0px) scale(1);
            }

            50% {
                transform: translateY(-25px) scale(1.15);
            }
        }


        /* =========================================
           MEDICAL AI SCANNER
        ========================================= */

        .medical-scanner {
            position: relative;
            width: 105px;
            height: 105px;
            margin: 5px auto 18px auto;
        }

        .scanner-ring {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            border: 2px solid rgba(56, 189, 248, 0.55);
            animation: scannerPulse 2.4s ease-out infinite;
        }

        .scanner-ring:nth-child(2) {
            animation-delay: 0.8s;
        }

        .scanner-ring:nth-child(3) {
            animation-delay: 1.6s;
        }

        @keyframes scannerPulse {

            0% {
                transform: scale(0.65);
                opacity: 0.9;
            }

            100% {
                transform: scale(1.45);
                opacity: 0;
            }
        }

        .scanner-core {
            position: absolute;
            width: 65px;
            height: 65px;
            top: 20px;
            left: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;

            background:
                radial-gradient(
                    circle,
                    rgba(56,189,248,0.30),
                    rgba(15,23,42,0.95)
                );

            border: 1px solid rgba(125,211,252,0.7);

            box-shadow:
                0 0 25px rgba(56,189,248,0.45),
                inset 0 0 20px rgba(56,189,248,0.15);

            animation: coreGlow 2.5s ease-in-out infinite;
        }

        @keyframes coreGlow {

            0%, 100% {
                box-shadow:
                    0 0 18px rgba(56,189,248,0.35),
                    inset 0 0 12px rgba(56,189,248,0.1);
            }

            50% {
                box-shadow:
                    0 0 35px rgba(56,189,248,0.75),
                    inset 0 0 20px rgba(56,189,248,0.25);
            }
        }

        .scanner-icon {
            font-size: 30px;
            animation: heartbeat 1.8s ease-in-out infinite;
        }

        @keyframes heartbeat {

            0%, 100% {
                transform: scale(1);
            }

            15% {
                transform: scale(1.15);
            }

            30% {
                transform: scale(1);
            }

            45% {
                transform: scale(1.08);
            }
        }


        /* =========================================
           TITLE
        ========================================= */

        .login-title {
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 4px;

            background: linear-gradient(
                90deg,
                #38bdf8,
                #818cf8,
                #38bdf8
            );

            background-size: 200% auto;

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            animation: titleGradient 4s linear infinite;
        }

        @keyframes titleGradient {

            0% {
                background-position: 0% center;
            }

            100% {
                background-position: 200% center;
            }
        }

        .login-subtitle {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 25px;
        }


        /* =========================================
           INPUT ANIMATION
        ========================================= */

        div[data-baseweb="input"] {
            transition: all 0.25s ease;
        }

        div[data-baseweb="input"]:focus-within {
            transform: translateY(-2px);

            box-shadow:
                0 0 0 1px rgba(56,189,248,0.65),
                0 0 18px rgba(56,189,248,0.18);
        }


        /* =========================================
           LOGIN BUTTON
        ========================================= */

        div.stButton > button {

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;

        }

        div.stButton > button:hover {

            transform: translateY(-3px);

            box-shadow:
                0 8px 25px rgba(56,189,248,0.22);

        }

        div.stButton > button:active {
            transform: translateY(0px) scale(0.98);
        }


        /* =========================================
           GOOGLE BUTTON
        ========================================= */

        a[data-testid="stLinkButton"] {

            transition:
                transform 0.25s ease,
                box-shadow 0.25s ease;

        }

        a[data-testid="stLinkButton"]:hover {

            transform: translateY(-3px);

            box-shadow:
                0 8px 25px rgba(66,133,244,0.20);

        }


        /* =========================================
           DIVIDER
        ========================================= */

        .login-divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 22px 0;
            color: #64748b;
            font-size: 12px;
        }

        .login-divider::before,
        .login-divider::after {

            content: "";
            flex: 1;
            height: 1px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(148,163,184,0.3),
                    transparent
                );
        }


        /* =========================================
           SECURITY BADGE
        ========================================= */

        .security-badge {

            display: inline-flex;
            align-items: center;
            gap: 7px;

            padding: 7px 13px;

            border-radius: 999px;

            background: rgba(15,23,42,0.55);

            border: 1px solid rgba(56,189,248,0.18);

            color: #94a3b8;

            font-size: 11px;

            margin-top: 18px;

        }

        .security-dot {

            width: 7px;
            height: 7px;
            border-radius: 50%;

            background: #22c55e;

            box-shadow:
                0 0 8px rgba(34,197,94,0.8);

            animation: securityPulse 1.8s infinite;
        }

        @keyframes securityPulse {

            0%, 100% {
                opacity: 1;
                transform: scale(1);
            }

            50% {
                opacity: 0.45;
                transform: scale(0.7);
            }
        }


        /* =========================================
           MOBILE
        ========================================= */

        @media (max-width: 600px) {

            .login-title {
                font-size: 28px;
            }

            .medical-scanner {
                width: 90px;
                height: 90px;
            }

            .scanner-core {
                width: 56px;
                height: 56px;
                top: 17px;
                left: 17px;
            }

            .scanner-icon {
                font-size: 25px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


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

        conn = get_connection()
        c = conn.cursor()

        backend = get_database_backend()

        email_placeholder = "?" if backend == "sqlite" else "%s"

        c.execute(
            f"""
            SELECT id, fullname, email
            FROM users
            WHERE email={email_placeholder}
            """,
            (email,)
        )

        user = c.fetchone()

        if user is None:

            user_placeholder = "?" if backend == "sqlite" else "%s"

            c.execute(
                f"""
                INSERT INTO users(
                fullname,
                email,
                password
            )
            VALUES({user_placeholder}, {user_placeholder}, {user_placeholder})
            """,
            (
                fullname,
                email,
                "GOOGLE_OAUTH_USER"
            )
        )

            conn.commit()

            c.execute(
                f"""
                SELECT id, fullname, email
                FROM users
                WHERE email={email_placeholder}
                """,
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

    except Exception as e:

        st.error(
            f"Google login failed: {e}"
        )

        return False


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    # Google callback must remain FIRST
    if google_callback():

        st.success(
            "Google Login Successful ✅"
        )

        st.rerun()

    # Animation CSS
    login_animation_css()

    # =====================================================
    # ANIMATED HERO
    # =====================================================

    st.html(
        """
        <div class="medical-scanner">

            <div class="scanner-ring"></div>
            <div class="scanner-ring"></div>
            <div class="scanner-ring"></div>

            <div class="scanner-core">
                <div class="scanner-icon">🩺</div>
            </div>

        </div>
        """
    )
    # =====================================================
    # LOGIN FORM
    # =====================================================

    email = st.text_input(
        "Email",
        key="login_email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
        placeholder="Enter your password"
    )

    if st.button(
        "🔐  Login to SkinAI Pro",
        key="login_button",
        use_container_width=True
    ):

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            SELECT id, fullname, email, password
            FROM users
            WHERE email=%s
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
    # DIVIDER
    # =====================================================

    st.markdown(
        """
        <div class="login-divider">
            OR CONTINUE WITH
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # GOOGLE
    # =====================================================

    google_login()

    # =====================================================
    # FACEBOOK
    # =====================================================

    if st.button(
        "📘  Continue with Facebook",
        use_container_width=True,
        key="facebook_login_button"
    ):

        st.info(
            "Facebook Login will be connected next."
        )

    # =====================================================
    # SECURITY
    # =====================================================

    st.markdown(
        """
        <div class="security-badge">
            <span class="security-dot"></span>
            Secure AI-powered authentication
        </div>
      """,
        unsafe_allow_html=True
    )