import streamlit as st
from auth.db import add_user, get_all_users
from auth.hash import hash_password

def show(authenticator):


    if st.session_state.get("authentication_status"):

        st.title("About Page")

        st.markdown("""
ADD CONTENT TO ABOUT PAGE 
        """)

        return   


    st.title("Welcome to Analytiq")

    choice = st.radio("Select Option", ["Login", "Sign Up"])

 
    if choice == "Login":


        st.session_state.pop("signup_success", None)

        authenticator.login()

        if st.session_state.get("authentication_status") is False:
            st.error("Invalid username or password")

        elif st.session_state.get("authentication_status") is None:
            st.info("Enter your credentials")


    else:
        st.subheader("Create Account")

        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        button_clicked = st.button("Sign Up")


        if button_clicked:

            users = [u[0] for u in get_all_users()]

            if username in users:
                st.error("Username already exists")

            elif name == "" or username == "" or password == "":
                st.error("Please fill all fields")

            else:
                hashed_pw = hash_password(password)
                add_user(username, name, hashed_pw)

         
                st.session_state["signup_success"] = True
                st.rerun()

 
        elif st.session_state.get("signup_success"):
            st.success("Account created! You can now log in.")

 
            st.session_state.pop("signup_success", None)