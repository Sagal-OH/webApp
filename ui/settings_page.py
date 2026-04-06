import streamlit as st

def show(authenticator):

    st.title("Settings")

 
    if not st.session_state.get("authentication_status"):
        st.warning("Please login first")
        return

  
    st.subheader("Account")

    st.write(f"Logged in as: **{st.session_state.get('name')}**")

    st.divider()

    st.subheader("Actions")

  
    authenticator.logout("Logout", "main")