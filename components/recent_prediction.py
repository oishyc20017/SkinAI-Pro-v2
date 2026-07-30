import streamlit as st

from services.dashboard_service import get_recent_prediction


def recent_prediction():

    user_id = st.session_state.user_id

    prediction = get_recent_prediction(user_id)

    st.subheader("📌 Recent Prediction")

    if prediction is None:

        st.info("No prediction yet.")

        return

    disease, confidence = prediction

    st.container(border=True)

    with st.container():

        st.markdown(f"### 🧬 {disease}")

        st.write(f"**Confidence:** {confidence}%")

        st.success("Latest prediction saved successfully.")