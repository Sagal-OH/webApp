import streamlit as st


def show(authenticator):
    if not st.session_state.get("authentication_status"):
        st.warning("Please log in to access this page.")
        return

    name     = st.session_state.get('name', 'User')
    username = st.session_state.get('username', '')

    st.title("Settings")
    st.markdown("---")

    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Username:** {username}")

    st.markdown("---")

    authenticator.logout("Logout", "main")