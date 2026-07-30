import streamlit as st

from services.dashboard_service import (
    get_recent_prediction,
    get_recent_chat,
    get_recent_booking
)


def dashboard_page():

    st.markdown("# 🩺 SkinAI Dashboard")

    st.caption(
        "Welcome to your SkinAI Pro dashboard."
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    # ---------------------------------
    # Recent Prediction
    # ---------------------------------

    prediction = get_recent_prediction(user_id)

    # ---------------------------------
    # Recent Chat
    # ---------------------------------

    recent_chat = get_recent_chat(user_id)

    # ---------------------------------
    # Recent Booking
    # ---------------------------------

    booking = get_recent_booking(user_id)

    # ---------------------------------
    # Dashboard Cards
    # ---------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔬 Recent Skin Analysis")

        if prediction:

            disease, confidence = prediction

            st.write(f"**Prediction:** {disease}")
            st.write(f"**Confidence:** {confidence}%")

        else:

            st.info("No skin analysis yet.")

    with col2:

        st.markdown("### 💬 Recent Chat")

        if recent_chat:

            st.write(
                recent_chat[0]
            )

        else:

            st.info("No chat messages yet.")

    with col3:

        st.markdown("### 👨‍⚕️ Recent Appointment")

        if booking:

            doctor_name, booking_date, booking_time = booking

            st.write(
                f"**Doctor:** {doctor_name}"
            )

            st.write(
                f"**Date:** {booking_date}"
            )

            st.write(
                f"**Time:** {booking_time}"
            )

        else:

            st.info("No appointment booked yet.")