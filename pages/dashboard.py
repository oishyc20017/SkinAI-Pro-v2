import streamlit as st

from services.dashboard_service import (
    get_recent_prediction,
    get_recent_chat,
    get_recent_booking
)


# =========================================================
# DASHBOARD ANIMATION / STYLE
# =========================================================

def dashboard_animation_css():

    st.markdown(
        """
        <style>

        /* =================================================
           DASHBOARD BACKGROUND
        ================================================= */

        .dashboard-hero {
            position: relative;
            padding: 25px 10px 30px 10px;
            overflow: hidden;
        }

        .dashboard-orb {
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            filter: blur(55px);
            opacity: 0.16;
            pointer-events: none;
            animation: dashboardFloat 7s ease-in-out infinite;
        }

        .dashboard-orb.one {
            background: #38bdf8;
            top: -60px;
            left: 8%;
        }

        .dashboard-orb.two {
            background: #8b5cf6;
            top: 40px;
            right: 8%;
            animation-delay: 2s;
        }

        @keyframes dashboardFloat {

            0%, 100% {
                transform: translateY(0px) scale(1);
            }

            50% {
                transform: translateY(-18px) scale(1.08);
            }
        }


        /* =================================================
           DASHBOARD TITLE
        ================================================= */

        .dashboard-title {
            position: relative;
            z-index: 2;
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .dashboard-subtitle {
            position: relative;
            z-index: 2;
            text-align: center;
            color: #94A3B8;
            font-size: 15px;
            margin-bottom: 20px;
        }


        /* =================================================
           DASHBOARD STATUS
        ================================================= */

        .dashboard-status {
            position: relative;
            z-index: 2;
            width: fit-content;
            margin: 0 auto 25px auto;
            padding: 7px 15px;
            border-radius: 999px;
            border: 1px solid rgba(56, 189, 248, 0.25);
            background: rgba(15, 23, 42, 0.55);
            color: #7dd3fc;
            font-size: 12px;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }

        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #22c55e;
            margin-right: 7px;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.7);
            animation: statusPulse 2s infinite;
        }

        @keyframes statusPulse {

            0%, 100% {
                opacity: 1;
                transform: scale(1);
            }

            50% {
                opacity: 0.45;
                transform: scale(0.75);
            }
        }


        /* =================================================
           STREAMLIT COLUMN CARDS
        ================================================= */

        div[data-testid="column"] {
            transition:
                transform 0.25s ease,
                filter 0.25s ease;
        }

        div[data-testid="column"]:hover {
            transform: translateY(-5px);
        }


        /* =================================================
           CARD CONTENT
        ================================================= */

        .dashboard-card {
            min-height: 190px;
            padding: 22px;
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.86),
                rgba(30, 41, 59, 0.62)
            );
            box-shadow:
                0 12px 35px rgba(0, 0, 0, 0.18);
            backdrop-filter: blur(12px);
            transition:
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }

        .dashboard-card:hover {
            border-color: rgba(56, 189, 248, 0.38);
            box-shadow:
                0 16px 42px rgba(0, 0, 0, 0.25),
                0 0 25px rgba(56, 189, 248, 0.07);
        }

        .card-icon {
            font-size: 30px;
            margin-bottom: 8px;
        }

        .card-title {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .card-label {
            color: #94A3B8;
            font-size: 13px;
            margin-top: 7px;
        }

        .card-value {
            font-size: 16px;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD PAGE
# =========================================================

def dashboard_page():

    dashboard_animation_css()

    # =====================================================
    # HERO
    # =====================================================

    st.html(
        """
        <div class="dashboard-hero">

            <div class="dashboard-orb one"></div>
            <div class="dashboard-orb two"></div>

            <div class="dashboard-title">
                🩺 SkinAI Dashboard
            </div>

            <div class="dashboard-subtitle">
                Welcome to your intelligent skin health companion.
            </div>

            <div class="dashboard-status">
                <span class="status-dot"></span>
                SkinAI AI System Online
            </div>

        </div>
        """
    )

    # =====================================================
    # USER CHECK
    # =====================================================

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")
        return

    # =====================================================
    # GET RECENT DATA
    # =====================================================

    prediction = get_recent_prediction(user_id)

    recent_chat = get_recent_chat(user_id)

    booking = get_recent_booking(user_id)

    # =====================================================
    # DASHBOARD CARDS
    # =====================================================
    st.markdown(
        """
        <style>

        .dashboard-card {
            padding: 22px;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.70);
            border: 1px solid rgba(148, 163, 184, 0.15);
            min-height: 190px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
            transition: transform 0.25s ease,
                        border-color 0.25s ease;
        }

        .dashboard-card:hover {
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.40);
        }

        .dashboard-icon {
            font-size: 30px;
            margin-bottom: 10px;
        }

        .dashboard-card-title {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .dashboard-value {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 7px;
        }

        .dashboard-label {
            color: #94A3B8;
            font-size: 13px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # RECENT PREDICTION
    # =====================================================

    with col1:

        prediction_text = "No skin analysis yet."
        confidence_text = ""

        if prediction:
            disease, confidence = prediction
            prediction_text = disease
            confidence_text = f"{confidence}% confidence"

        st.html(f"""
        <div class="dashboard-card">

            <div class="dashboard-icon">🔬</div>

            <div class="dashboard-card-title">
                Recent Skin Analysis
            </div>

            <div class="dashboard-value">
                {prediction_text}
            </div>

            <div class="dashboard-label">
                {confidence_text}
            </div>

        </div>
        """)
    # =====================================================
    # RECENT CHAT
    # =====================================================

    with col2:

        chat_text = "No chat messages yet."

        if recent_chat:
            chat_text = recent_chat[0]

        st.html(f"""
        <div class="dashboard-card">

            <div class="dashboard-icon">💬</div>

            <div class="dashboard-card-title">
                Recent Chat
            </div>

            <div class="dashboard-value">
                AI Assistant
            </div>

            <div class="dashboard-label">
                {chat_text}
            </div>

        </div>
        """)

    # =====================================================
    # RECENT BOOKING
    # =====================================================

    with col3:

        if booking:

            doctor_name, booking_date, booking_time, status = booking

            booking_html = f"""
            <div class="dashboard-value">
                {doctor_name}
            </div>

            <div class="dashboard-label">
                📅 {booking_date}
                <br>
                🕐 {booking_time}
            </div>
            """

        else:

            booking_html = """
            <div class="dashboard-value">
                No appointment
            </div>

            <div class="dashboard-label">
                No appointment booked yet.
            </div>
            """

        st.html(f"""
        <div class="dashboard-card">

            <div class="dashboard-icon">
                🩺
            </div>

            <div class="dashboard-card-title">
                Recent Appointment
            </div>

            {booking_html}

        </div>
        """)
