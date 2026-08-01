import streamlit as st

from database.db import get_connection


def admin_page():

    st.title("🛠️ SkinAI Pro Admin Dashboard")
    st.caption("Database monitoring and management")

    # ==========================================
    # ADMIN ACCESS
    # ==========================================

    admin_email = st.secrets.get(
        "ADMIN_EMAIL",
        ""
    ).strip().lower()

    current_email = st.session_state.get(
        "email",
        ""
    ).strip().lower()

    if not st.session_state.get("logged_in", False):
        st.error("Please login first.")
        return

    if not admin_email or current_email != admin_email:
        st.error("⛔ Access Denied")
        st.warning(
            "You do not have permission to access the Admin Dashboard."
        )
        return

    # ==========================================
    # REFRESH
    # ==========================================

    col1, col2 = st.columns([1, 5])

    with col1:

        if st.button(
            "🔄 Refresh",
            use_container_width=True
        ):

            st.rerun()

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    try:

        conn = get_connection()

    except Exception as e:

        st.error(
            f"Could not connect to Neon database: {e}"
        )

        return

    # ==========================================
    # DATABASE DATA
    # ==========================================

    try:

        # ======================================
        # COUNTS
        # ======================================

        users_count = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        predictions_count = conn.execute(
            "SELECT COUNT(*) FROM prediction_history"
        ).fetchone()[0]

        conversations_count = conn.execute(
            "SELECT COUNT(*) FROM conversations"
        ).fetchone()[0]

        messages_count = conn.execute(
            "SELECT COUNT(*) FROM messages"
        ).fetchone()[0]

        bookings_count = conn.execute(
            "SELECT COUNT(*) FROM bookings"
        ).fetchone()[0]

        # ======================================
        # STAT CARDS
        # ======================================

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "👤 Users",
            users_count
        )

        c2.metric(
            "🔬 Predictions",
            predictions_count
        )

        c3.metric(
            "💬 Conversations",
            conversations_count
        )

        c4.metric(
            "📨 Messages",
            messages_count
        )

        c5.metric(
            "📅 Bookings",
            bookings_count
        )

        st.divider()

        # ======================================
        # USERS
        # ======================================

        st.subheader("👤 Registered Users")

        users = conn.execute(
            """
            SELECT
                id,
                fullname,
                email,
                created_at
            FROM users
            ORDER BY id DESC
            """
        ).fetchall()

        if users:

            st.dataframe(
                users,
                column_config={
                    "id": "ID",
                    "fullname": "Full Name",
                    "email": "Email",
                    "created_at": "Created At"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No users found.")

        # ======================================
        # BOOKINGS
        # ======================================

        st.subheader("📅 Doctor Bookings")

        bookings = conn.execute(
            """
            SELECT
                id,
                user_id,
                doctor_name,
                specialty,
                hospital_name,
                patient_name,
                patient_email,
                phone,
                booking_date,
                booking_time,
                symptoms,
                payment_method,
                status,
                created_at
            FROM bookings
            ORDER BY id DESC
            """
        ).fetchall()

        if bookings:

            st.dataframe(
                bookings,
                column_config={
                    "id": "ID",
                    "user_id": "User ID",
                    "doctor_name": "Doctor",
                    "specialty": "Specialty",
                    "hospital_name": "Hospital",
                    "patient_name": "Patient",
                    "patient_email": "Email",
                    "phone": "Phone",
                    "booking_date": "Date",
                    "booking_time": "Time",
                    "symptoms": "Symptoms",
                    "payment_method": "Payment",
                    "status": "Status",
                    "created_at": "Created At"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No bookings found.")

        # ======================================
        # PREDICTION HISTORY
        # ======================================

        st.subheader("🔬 Prediction History")

        predictions = conn.execute(
            """
            SELECT
                id,
                user_id,
                disease,
                confidence,
                image_path,
                created_at
            FROM prediction_history
            ORDER BY id DESC
            """
        ).fetchall()

        if predictions:

            st.dataframe(
                predictions,
                column_config={
                    "id": "ID",
                    "user_id": "User ID",
                    "disease": "Disease",
                    "confidence": "Confidence",
                    "image_path": "Image",
                    "created_at": "Created At"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No prediction history found.")

        # ======================================
        # CONVERSATIONS
        # ======================================

        st.subheader("💬 Conversations")

        conversations = conn.execute(
            """
            SELECT
                id,
                user_id,
                title,
                created_at
            FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()

        if conversations:

            st.dataframe(
                conversations,
                column_config={
                    "id": "Conversation ID",
                    "user_id": "User ID",
                    "title": "Title",
                    "created_at": "Created At"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No conversations found.")

        # ======================================
        # MESSAGES
        # ======================================

        st.subheader("📨 Messages")

        messages = conn.execute(
            """
            SELECT
                id,
                conversation_id,
                user_id,
                role,
                message,
                created_at
            FROM messages
            ORDER BY id DESC
            """
        ).fetchall()

        if messages:

            st.dataframe(
                messages,
                column_config={
                    "id": "Message ID",
                    "conversation_id": "Conversation ID",
                    "user_id": "User ID",
                    "role": "Role",
                    "message": "Message",
                    "created_at": "Created At"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No messages found.")

    except Exception as e:

        st.error(
            f"Database error: {e}"
        )

    finally:

        conn.close()