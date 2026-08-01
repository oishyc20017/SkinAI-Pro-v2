import streamlit as st

from services.history_service import (
    get_prediction_history,
    delete_prediction
)

from services.chat_service import (
    load_conversations,
    load_messages
)

from database.db import get_connection
from utils.time_utils import format_bd_time


def get_booking_history(user_id):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT
            id,
            doctor_name,
            booking_date,
            booking_time,
            status,
            patient_name,
            patient_email,
            phone,
            specialty,
            hospital_name,
            symptoms,
            payment_method,
            created_at
        FROM bookings
        WHERE user_id=%s
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = c.fetchall()

    conn.close()

    return rows


def history_page():

    st.markdown("## 📜 History")

    st.caption(
        "View your previous predictions, AI conversations, and bookings."
    )

    prediction_tab, chat_tab, booking_tab = st.tabs(
        [
            "🔬 Predictions",
            "💬 AI Chats",
            "👨‍⚕️ Bookings"
        ]
    )

    # =========================================================
    # PREDICTION HISTORY
    # =========================================================

    with prediction_tab:

        predictions = get_prediction_history(
            st.session_state.user_id
        )

        if len(predictions) == 0:

            st.info(
                "🔬 No prediction history found yet."
            )

        else:

            st.markdown(
                f"**{len(predictions)} prediction(s) found**"
            )

            for item in predictions:

                prediction_id = item[0]
                disease = item[1]
                confidence = item[2]
                created = item[3]

                with st.container(border=True):

                    col1, col2 = st.columns([3, 1])

                    with col1:

                        st.markdown(
                            f"### 🧬 {disease}"
                        )

                        st.caption(
                            f"Analyzed on {created}"
                        )

                    with col2:

                        st.metric(
                            "Confidence",
                            f"{confidence}%"
                        )

                    st.divider()

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{prediction_id}",
                        use_container_width=True
                    ):

                        delete_prediction(
                            prediction_id
                        )

                        st.success(
                            "Prediction deleted."
                        )

                        st.rerun()
    # =========================================================
    # AI CHAT HISTORY
    # =========================================================

    with chat_tab:

        conversations = load_conversations(
            st.session_state.user_id
        )

        if not conversations:

            st.info(
                "💬 No AI chat history found yet."
            )

        else:

            st.markdown(
                f"**{len(conversations)} conversation(s) found**"
            )

            for conversation_id, title in conversations:

                messages = load_messages(
                    conversation_id
                )

                with st.container(border=True):

                    # -----------------------------------------
                    # Conversation Header
                    # -----------------------------------------

                    col1, col2 = st.columns(
                        [5, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 💬 {title or 'New Chat'}"
                        )

                    with col2:

                        st.caption(
                            f"ID: {conversation_id}"
                        )

                    # -----------------------------------------
                    # Messages
                    # -----------------------------------------

                    if messages:

                        last_user_message = None
                        last_ai_message = None

                        for role, message, created_at in messages:

                            if role == "user":
                                last_user_message = message

                            elif role == "assistant":
                                last_ai_message = message
                        if last_user_message:

                            preview = last_user_message

                            if len(preview) > 100:
                                preview = preview[:100] + "..."

                            st.markdown(
                                f"**You:** {preview}"
                            )

                        if last_ai_message:

                            preview = last_ai_message

                            if len(preview) > 150:
                                preview = preview[:150] + "..."

                            st.markdown(
                                f"**SkinAI:** {preview}"
                            )

                        st.caption(
                            f"💬 {len(messages)} message(s)"
                        )

                    else:

                        st.caption(
                            "No messages in this conversation."
                        )

                    # -----------------------------------------
                    # Open Conversation
                    # -----------------------------------------

                    if st.button(
                        "Open Conversation",
                        use_container_width=True,
                        key=f"history_chat_{conversation_id}"
                    ):

                        st.session_state.current_conversation_id = (
                            conversation_id
                        )

                        st.session_state.messages = []

                        for role, message, created_at in messages:

                            st.session_state.messages.append(
                                {
                                    "role": role,
                                    "content": message
                                }
                            )

                        st.session_state.page = "chat"

                        st.rerun()
    # =========================================================
    # BOOKING HISTORY
    # =========================================================

    with booking_tab:

        bookings = get_booking_history(
            st.session_state.user_id
        )

        if not bookings:

            st.info(
                "👨‍⚕️ No doctor bookings found yet."
            )

        else:

            st.markdown(
                f"**{len(bookings)} appointment(s) found**"
            )

            for booking in bookings:

                (
                    booking_id,
                    doctor_name,
                    booking_date,
                    booking_time,
                    status,
                    patient_name,
                    patient_email,
                    phone,
                    specialty,
                    hospital_name,
                    symptoms,
                    payment_method,
                    created_at
                ) = booking

                with st.container(border=True):

                    st.markdown(
                        f"### 👨‍⚕️ {doctor_name}"
                    )

                    st.caption(
                        f"{specialty} • {hospital_name}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"📅 **Date:** {booking_date}"
                        )

                        st.write(
                            f"🕐 **Time:** {booking_time}"
                        )

                        st.write(
                            f"👤 **Patient:** {patient_name}"
                        )

                        st.write(
                            f"📱 **Phone:** {phone}"
                        )

                    with col2:

                        st.write(
                            f"📧 **Email:** {patient_email}"
                        )

                        st.write(
                            f"💳 **Payment:** {payment_method}"
                        )

                        st.write(
                            f"📌 **Status:** {status}"
                        )

                        st.caption(
                            f"Booked on {format_bd_time(created_at)}"
                        )

                    if symptoms:

                        st.markdown("**📝 Reason for Visit**")

                        st.write(symptoms)