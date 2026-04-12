import streamlit as st
from auth.db import add_user, get_all_users
from auth.hash import hash_password

def show(authenticator):


    if st.session_state.get("authentication_status"):

        st.title("About Page")

        st.markdown("""
                    
Analytiq is a customer analytics platform that helps retail businesses 
make smarter decisions - faster.

---

### What Analytiq offers

**Dashboard :**
A real-time overview of your revenue, customer activity and sales trends in one place.

**Customer Segments :**
Understand who your customers are , your most loyal buyers, occasional shoppers 
and accounts that need attention, all automatically identified for you.

**Churn Prediction :**
Know which customers are at risk of leaving before they do - so you can take 
action at the right time.

**Suspicious Transactions :**
Stay in control of your data. Unusual orders are automatically flagged so 
nothing slips through the cracks.

---

### Security
All accounts are password protected. Your data is only accessible to you.

---

*Analytiq - Built for smarter business decisions.*





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
