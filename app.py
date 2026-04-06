import streamlit as st
from streamlit_option_menu import option_menu
from auth.db import create_users_table
from auth.auth_service import get_authenticator
from ui import landing_page, settings_page

st.set_page_config(page_title="Analytiq", layout="wide")

create_users_table()

authenticator = get_authenticator()


with st.sidebar:
    selected = option_menu(
        None,
        ["Home", "Dashboard", "Customer Insights", "Fraud Detection", "AnalytiqAI", "Settings"],
        icons=["house", "bar-chart","people", "shield-lock", "robot", "gear"],
    )


if selected == "Home":
    landing_page.show(authenticator)

elif selected == "Settings":
    settings_page.show(authenticator)