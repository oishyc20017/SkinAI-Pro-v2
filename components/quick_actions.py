import streamlit as st


def action_card(icon, title, description, page):

    with st.container(border=True):

        st.markdown(f"## {icon}")

        st.subheader(title)

        st.caption(description)

        if st.button(
            f"Open {title}",
            key=f"action_{page}",
            use_container_width=True
        ):
            st.session_state.page = page
            st.rerun()


def quick_actions():

    st.markdown("## ⚡ Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        action_card(
            "🔬",
            "Skin Analysis",
            "Upload an image and detect skin disease.",
            "prediction"
        )

        action_card(
            "👨‍⚕️",
            "Doctor Booking",
            "Book an appointment with a dermatologist.",
            "booking"
        )

    with col2:

        action_card(
            "💬",
            "AI Assistant",
            "Ask AI anything about skin care.",
            "chat"
        )

        action_card(
            "📜",
            "History",
            "View previous predictions and chats.",
            "history"
        )