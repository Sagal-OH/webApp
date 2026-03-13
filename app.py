
import streamlit as st
from streamlit_option_menu import option_menu

from ui import landingPage
from ui import aboutPage



st.set_page_config(page_title="Analytiq", layout="wide")


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Landing", "About", "Dashboard", "Churn Prediction", "Fraud Detection", "Customer Segment", "Settings"],
        default_index=0
    )


if selected == "Landing":
    landingPage.show()

#elif selected == "About":
   # aboutPage.show()







