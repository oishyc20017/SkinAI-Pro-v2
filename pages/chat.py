import streamlit as st

from components.chat_bubble import chat_bubble
from services.chat_service import (
    create_conversation,
    save_message,
    update_conversation_title,
    load_messages
)
from services.ai_service import ask_ai


def chat_page():

    # -----------------------------
    # Session State
    # -----------------------------

    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -----------------------------
    # Load Existing Messages
    # -----------------------------

    if (
        st.session_state.current_conversation_id
        and not st.session_state.messages
    ):
        rows = load_messages(
            st.session_state.current_conversation_id
        )

        for role, message, created_at in rows:
            st.session_state.messages.append({
                "role": role,
                "content": message
            })

    # -----------------------------
    # Header / Welcome
    # -----------------------------

    if st.session_state.current_conversation_id:

        st.markdown(
            """
<div class="chat-header">
    <div class="chat-header-icon">🩺</div>
    <div>
        <div class="chat-header-title">
            SkinAI Assistant
        </div>
        <div class="chat-header-subtitle">
            Your AI skin health assistant
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
<div class="chat-welcome">
    <div class="chat-welcome-icon">🩺</div>
    <h1>How can I help you today?</h1>
    <p>
        Ask SkinAI about skin diseases, skincare,
        or your skin analysis.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    # -----------------------------
    # Previous Messages
    # -----------------------------

    for msg in st.session_state.messages:

        chat_bubble(
            msg["role"],
            msg["content"]
        )

    # -----------------------------
    # Chat Input
    # -----------------------------

    prompt = st.chat_input(
        "Message SkinAI..."
    )

    if not prompt:
        return

    # -----------------------------
    # Create Conversation
    # -----------------------------

    if st.session_state.current_conversation_id is None:

        conversation_id = create_conversation(
            st.session_state.user_id,
            "New Chat"
        )

        st.session_state.current_conversation_id = conversation_id

    # -----------------------------
    # Save User Message
    # -----------------------------

    save_message(
        st.session_state.current_conversation_id,
        st.session_state.user_id,
        "user",
        prompt
    )

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # -----------------------------
    # AI Response
    # -----------------------------

    with st.spinner("SkinAI is thinking..."):

        ai_reply = ask_ai(prompt)

    # -----------------------------
    # Save AI Response
    # -----------------------------

    save_message(
        st.session_state.current_conversation_id,
        st.session_state.user_id,
        "assistant",
        ai_reply
    )

    # -----------------------------
    # Update Conversation Title
    # -----------------------------

    update_conversation_title(
        st.session_state.current_conversation_id,
        prompt[:40]
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()