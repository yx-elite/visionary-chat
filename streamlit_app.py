import streamlit as st
from datetime import datetime
from session_state import init_session_state


# Setup app configurations
st.set_page_config(
    page_title="Visionary AI Chat",
    page_icon="🔗",
    layout='wide'
)

# ------ Page Setup ------
api_usage = st.Page(
    'pages/api_usage.py',
    title="API Usage",
    icon=':material/data_usage:',
)

# ------ Navigation Setup ------
nav = st.navigation(
    {
        "CHATBOT": [],
        "OTHERS": [api_usage]
    }
)

# ------ Shared Widgets ------
@st.cache_data
def fetch_modified_date():
    return datetime.now().strftime('%b %d, %Y')

init_session_state()

author = "[YX-ELITE](https://github.com/yx-elite)"
dark_theme_logo = './static/langchain-logo-text-dark.png'
modified_date = fetch_modified_date()

st.logo(dark_theme_logo)
st.sidebar.caption(f"Last Updated on {modified_date} by - {author} -")
nav.run()