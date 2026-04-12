import streamlit as st
from streamlit_option_menu import option_menu
from auth.db import create_users_table
from auth.auth_service import get_authenticator
from ui import landing_page, settings_page,dashboard_page,suspiciousTransaction_page,customerSegments_page,customerRetention_page

st.set_page_config(page_title="Analytiq", layout="wide")

create_users_table()

authenticator = get_authenticator()


with st.sidebar:
    selected = option_menu(
        None,
        ["Home", "Dashboard", "Customer Segments", "Customer Retention", "Suspicious Transactions", "Settings"],
        icons=["house", "bar-chart-line", "people", "person-check", "exclamation-triangle", "gear"],
    )


if selected == "Home":
    landing_page.show(authenticator)
    
elif selected == "Dashboard":
    dashboard_page.show()

elif selected == "Customer Segments":
    customerSegments_page.show()

elif selected == "Customer Retention":
    customerRetention_page.show()

elif selected == "Suspicious Transactions":
    suspiciousTransaction_page.show()

elif selected == "Settings":
    settings_page.show(authenticator)