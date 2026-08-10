import sqlite3
from pathlib import Path
import streamlit as st
from datetime import date

from database.db import get_connection
from utils.time_utils import get_bd_time


# =========================================================
# SQLITE DATABASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "skinai.db"


def get_sqlite_connection():

    conn = sqlite3.connect(
        str(SQLITE_DB_PATH),
        check_same_thread=False
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# BOOKING PAGE
# =========================================================

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

    # =====================================================
    # DOCTOR INFORMATION
    # =====================================================

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

    # =====================================================
    # PATIENT INFORMATION
    # =====================================================

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

    # =====================================================
    # APPOINTMENT INFORMATION
    # =====================================================

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

    # =====================================================
    # APPOINTMENT SUMMARY
    # =====================================================

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

        st.write(
            f"**Time:** {booking_time}"
        )

        st.write(
            f"**Payment:** {payment_method}"
        )

    st.write("")

    # =====================================================
    # CONFIRM BOOKING
    # =====================================================

    if st.button(
        "📅 Confirm Appointment",
        use_container_width=True,
        key="confirm_booking"
    ):

        # -------------------------------------------------
        # LOGIN CHECK
        # -------------------------------------------------

        if not st.session_state.get(
            "logged_in",
            False
        ):

            st.warning(
                "Please login before booking an appointment."
            )

            return

        # -------------------------------------------------
        # PHONE CHECK
        # -------------------------------------------------

        if not phone.strip():

            st.warning(
                "Please enter your phone number."
            )

            return

        # -------------------------------------------------
        # SYMPTOMS CHECK
        # -------------------------------------------------

        if not symptoms.strip():

            st.warning(
                "Please describe your symptoms or reason for visit."
            )

            return

        # =================================================
        # BOOKING DATA
        # =================================================

        user_id = st.session_state.user_id

        booking_date_value = booking_date.strftime(
            "%Y-%m-%d"
        )

        created_at = get_bd_time()

        status = "Pending"

        # =================================================
        # 1. SAVE BOOKING TO NEON
        # =================================================

        neon_conn = get_connection()

        try:

            with neon_conn.cursor() as c:

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
                    VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        user_id,
                        doctor_name,
                        booking_date_value,
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
                )

                booking_id = c.fetchone()[0]

            neon_conn.commit()

        except Exception as e:

            neon_conn.rollback()

            st.error(
                f"Booking failed: {e}"
            )

            return

        finally:

            neon_conn.close()

        # =================================================
        # 2. SAVE SAME BOOKING TO SQLITE IMMEDIATELY
        # =================================================

        sqlite_conn = get_sqlite_connection()

        try:

            sqlite_conn.execute(
                """
                INSERT OR IGNORE INTO bookings(
                    id,
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
                VALUES(
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    booking_id,
                    user_id,
                    doctor_name,
                    booking_date_value,
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
            )

            sqlite_conn.commit()

        except Exception as e:

            sqlite_conn.rollback()

            st.warning(
                "Booking was saved successfully, "
                "but local SQLite sync failed. "
                "The automatic Neon → SQLite sync will recover it."
            )

            print(
                "SQLite booking sync error:",
                e
            )

        finally:

            sqlite_conn.close()

        # =================================================
        # SUCCESS
        # =================================================

        st.success(
            "Appointment booked successfully! ✅"
        )