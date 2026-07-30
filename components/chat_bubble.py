import streamlit as st


def chat_bubble(role, content, created_at=None):

    if role == "user":

        with st.chat_message("user", avatar="👤"):

            st.markdown(
                f"""
<div class="user-message">
    {content}
</div>
""",
                unsafe_allow_html=True
            )

    else:

        with st.chat_message("assistant", avatar="🩺"):

            st.markdown(
                f"""
<div class="assistant-message">
    {content}
</div>
""",
                unsafe_allow_html=True
            )