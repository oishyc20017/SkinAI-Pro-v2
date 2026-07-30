import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="SkinAI Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database.schema import create_tables
from components.sidebar import sidebar
from components.theme import analysis_completed

from auth.register import register_page
from auth.login import login_page
from auth.logout import logout
from components.auth_layout import auth_header

from pages.dashboard import dashboard_page
from pages.chat import chat_page
from pages.prediction import prediction_page
from pages.booking import booking_page
from pages.history import history_page

create_tables()
css_file = Path("assets/css/style.css")

if css_file.exists():

    with open(css_file) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False

st.title("🩺 SkinAI Pro")

sidebar()

if st.session_state.logged_in:

    if "page" not in st.session_state:
        st.session_state.page = "chat"

    if st.session_state.page == "chat":
        chat_page()

    elif st.session_state.page == "prediction":
        prediction_page()

    elif st.session_state.page == "booking":
        booking_page()

    elif st.session_state.page == "history":
        history_page()

    # show success message if analysis finished elsewhere
    if st.session_state.get("analysis_completed"):
        analysis_completed()

else:
     
    auth_header()

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Register"
        ]
    )

    with tab1:
        login_page()

    with tab2:
        register_page()