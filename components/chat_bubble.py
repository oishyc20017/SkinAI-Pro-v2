import re
import html
import streamlit as st


def format_message(content):
    """
    Convert basic Markdown formatting from AI responses
    into HTML while keeping the existing chat bubble design.
    """

    # Convert content to safe HTML
    text = html.escape(str(content))

    # Convert **bold** → <strong>bold</strong>
    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        text
    )

    # Preserve line breaks
    text = text.replace("\n", "<br>")

    return text


def chat_bubble(role, content, created_at=None):

    formatted_content = format_message(content)

    if role == "user":

        with st.chat_message("user", avatar="👤"):

            st.markdown(
                f"""
<div class="user-message">
    {formatted_content}
</div>
""",
                unsafe_allow_html=True
            )

    else:

        with st.chat_message("assistant", avatar="🩺"):

            st.markdown(
                f"""
<div class="assistant-message">
    {formatted_content}
</div>
""",
                unsafe_allow_html=True
            )