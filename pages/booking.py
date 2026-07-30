import streamlit as st
from datetime import date

from database.db import get_connection
from utils.time_utils import get_bd_time


def booking_page():

    st.markdown(
        """
        <div class="booking-header">
            <h1>👨‍⚕️ Doctor Appointment</h1>
            <p>Book an appointment with a dermatologist.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------
    # Doctor Information
    # ---------------------------------

    doctors = {
        "Dr. Sarah Ahmed": {
            "specialty": "Dermatologist",
            "hospital": "Skin Care Medical Center"
        },
        "Dr. Nusrat Jahan": {
            "specialty": "Skin Specialist",
            "hospital": "Dermatology Care Hospital"
        },
        "Dr. Tanvir Hasan": {
            "specialty": "Dermatologist",
            "hospital": "City Skin & Laser Clinic"
        }
    }

    st.markdown("### 👨‍⚕️ Doctor Information")

    col1, col2 = st.columns(2)

    with col1:

        doctor_name = st.selectbox(
            "Select Doctor",
            list(doctors.keys()),
            key="booking_doctor"
        )

        specialty = doctors[doctor_name]["specialty"]

    with col2:

        st.text_input(
            "Specialty",
            value=specialty,
            disabled=True,
            key="booking_specialty"
        )

    hospital_name = doctors[doctor_name]["hospital"]

    st.text_input(
        "🏥 Hospital / Clinic",
        value=hospital_name,
        disabled=True,
        key="booking_hospital"
    )

    st.divider()

    # ---------------------------------
    # Patient Information
    # ---------------------------------

    st.markdown("### 👤 Patient Information")

    patient_name = st.session_state.get(
        "fullname",
        ""
    )

    patient_email = st.session_state.get(
        "email",
        ""
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Patient Name",
            value=patient_name,
            disabled=True,
            key="patient_name"
        )

    with col2:

        st.text_input(
            "Email",
            value=patient_email,
            disabled=True,
            key="patient_email"
        )

    phone = st.text_input(
        "📱 Phone Number",
        placeholder="Enter your phone number",
        key="booking_phone"
    )

    st.divider()

    # ---------------------------------
    # Appointment Information
    # ---------------------------------

    st.markdown("### 📅 Appointment Details")

    col1, col2 = st.columns(2)

    with col1:

        booking_date = st.date_input(
            "Appointment Date",
            min_value=date.today(),
            key="booking_date"
        )

    with col2:

        booking_time = st.selectbox(
            "Appointment Time",
            [
                "10:00 AM",
                "11:00 AM",
                "12:00 PM",
                "02:00 PM",
                "03:00 PM",
                "04:00 PM"
            ],
            key="booking_time"
        )

    symptoms = st.text_area(
        "📝 Symptoms / Reason for Visit",
        placeholder="Briefly describe your skin concern...",
        height=120,
        key="booking_symptoms"
    )

    payment_method = st.selectbox(
        "💳 Payment Method",
        [
            "Pay at Clinic",
            "Online Payment"
        ],
        key="booking_payment"
    )

    st.divider()

    # ---------------------------------
    # Appointment Summary
    # ---------------------------------

    st.markdown("### 📋 Appointment Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Doctor:** {doctor_name}")
        st.write(f"**Specialty:** {specialty}")
        st.write(f"**Hospital:** {hospital_name}")

    with col2:

        st.write(
            f"**Date:** {booking_date.strftime('%d %B %Y')}"
        )
        st.write(f"**Time:** {booking_time}")
        st.write(f"**Payment:** {payment_method}")

    st.write("")

    # ---------------------------------
    # Confirm Booking
    # ---------------------------------

    if st.button(
        "📅 Confirm Appointment",
        use_container_width=True,
        key="confirm_booking"
    ):

        if not st.session_state.get(
            "logged_in",
            False
        ):

            st.warning(
                "Please login before booking an appointment."
            )

            return

        if not phone.strip():

            st.warning(
                "Please enter your phone number."
            )

            return

        if not symptoms.strip():

            st.warning(
                "Please describe your symptoms or reason for visit."
            )

            return

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            INSERT INTO bookings(
                user_id,
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
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                st.session_state.user_id,
                doctor_name,
                booking_date.strftime("%Y-%m-%d"),
                booking_time,
                "Pending",
                patient_name,
                patient_email,
                phone,
                specialty,
                hospital_name,
                symptoms,
                payment_method,
                get_bd_time()
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "Appointment booked successfully! ✅"
        )