import streamlit as st

from auth.logout import logout
from services.chat_service import (
    load_conversations,
    load_messages
)


def menu_button(icon, title, page):

    if st.button(
        f"{icon}  {title}",
        use_container_width=True,
        key=f"menu_{page}"
    ):

        st.session_state.page = page
        st.rerun()


def sidebar():

    with st.sidebar:

        # ==============================
        # BRAND
        # ==============================

        st.markdown(
            """
            <div style="
                padding: 8px 4px 18px 4px;
            ">
                <div style="
                    font-size:25px;
                    font-weight:800;
                    color:white;
                ">
                    🩺 SkinAI Pro
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==============================
        # NEW CHAT
        # ==============================

        if st.button(
            "✨  New Chat",
            use_container_width=True,
            key="new_chat"
        ):

            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.session_state.page = "chat"

            st.rerun()

        st.divider()

        # ==============================
        # MAIN NAVIGATION
        # ==============================

        menu_button(
            "🔬",
            "Skin Analysis",
            "prediction"
        )

        menu_button(
            "💬",
            "AI Assistant",
            "chat"
        )

        menu_button(
            "📅",
            "Doctor Booking",
            "booking"
        )

        menu_button(
            "📜",
            "History",
            "history"
        )
                # ==============================
        # ADMIN DASHBOARD
        # ==============================

        admin_email = st.secrets.get(
            "ADMIN_EMAIL",
            ""
        ).strip().lower()

        current_email = st.session_state.get(
            "email",
            ""
        ).strip().lower()

        if (
            st.session_state.get("logged_in", False)
            and admin_email
            and current_email == admin_email
        ):

            menu_button(
                "🛠️",
                "Admin Dashboard",
                "admin"
            )

        # ==============================
        # RECENT CHATS
        # ==============================

        if st.session_state.get("logged_in", False):

            chats = load_conversations(
                st.session_state.user_id
            )

            if chats:

                st.divider()

                st.markdown(
                    "### 💬 Recent Chats"
                )

                for chat in chats[:5]:

                    conversation_id = chat[0]
                    title = chat[1]

                    if not title:
                        title = "New Chat"

                    if len(title) > 28:
                        title = title[:28] + "..."

                    if st.button(
                        f"💬  {title}",
                        use_container_width=True,
                        key=f"recent_chat_{conversation_id}"
                    ):

                        st.session_state.current_conversation_id = (
                            conversation_id
                        )

                        rows = load_messages(
                            conversation_id
                        )

                        st.session_state.messages = []

                        for role, message, created_at in rows:

                            st.session_state.messages.append(
                                {
                                    "role": role,
                                    "content": message
                                }
                            )

                        st.session_state.page = "chat"

                        st.rerun()

        # ==============================
        # ACCOUNT
        # ==============================

        st.divider()

        if st.session_state.get("logged_in", False):

            st.caption(
                f"Signed in as {st.session_state.get('fullname', 'User')}"
            )

            if st.button(
                "🚪  Logout",
                use_container_width=True,
                key="sidebar_logout"
            ):
                logout()