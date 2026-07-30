import streamlit as st

def auth_header():

    st.markdown(
        """
        <div style="margin-top:-10px;margin-bottom:25px;">
            <p style="
                color:#94A3B8;
                font-size:18px;
                margin:0;
            ">
                AI Powered Skin Disease Detection
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )