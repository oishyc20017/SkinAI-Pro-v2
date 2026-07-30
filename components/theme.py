import streamlit as st


def page_title(title):

    st.markdown(
        f"""
        <h2 style="
        margin-top:10px;
        margin-bottom:25px;
        ">
        {title}
        </h2>
        """,
        unsafe_allow_html=True
    )


def analysis_completed(message: str = "Analysis Completed ✅"):
    """Show a success message for completed analysis."""
    st.success(message)