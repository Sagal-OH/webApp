
import streamlit as st


def show():
    st.title('Welcome to :blue[Analytiq]')
    
    option = st.radio("Login/Signup", ["Login", "Sign Up"])

    if option == 'Login':
        
        emailAddress = st.text_input('Email Address', key="login_email")
        password = st.text_input('Password', type='password', key="login_password")

        st.button('Login')
        
    else:
        emailAddress = st.text_input('Email Address', key="signup_email")
        password = st.text_input('Password', type='password', key="signup_password")
        
        st.button('Create Account')









