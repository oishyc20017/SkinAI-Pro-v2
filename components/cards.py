import streamlit as st

def stat_card(title, value, icon):

    st.markdown(
        f"""
<div style="background:#1E293B;
padding:25px;
border-radius:18px;
border:1px solid #334155;
text-align:center;">

<div style="font-size:40px;">
{icon}
</div>

<h2 style="color:white;margin:10px 0;">
{value}
</h2>

<p style="color:#94A3B8;font-size:18px;">
{title}
</p>

</div>
""",
        unsafe_allow_html=True
    )