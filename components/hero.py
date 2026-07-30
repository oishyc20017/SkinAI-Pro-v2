import streamlit as st
from datetime import datetime


def hero():

    hour = datetime.now().hour

    if hour < 12:
        greet = "Good Morning ☀️"

    elif hour < 17:
        greet = "Good Afternoon 🌤️"

    else:
        greet = "Good Evening 🌙"

    st.markdown(
        f"""
<div style="
background:linear-gradient(135deg,#2563EB,#1D4ED8);
padding:35px;
border-radius:22px;
color:white;
margin-bottom:25px;
">

<h2 style="margin:0;">
{greet}, {st.session_state.fullname}
</h2>

<p style="font-size:18px;margin-top:10px;">
Welcome back to SkinAI Pro.
Your AI healthcare assistant is ready to help you.
</p>

</div>
""",
        unsafe_allow_html=True
    )