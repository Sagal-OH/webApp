import streamlit_authenticator as stauth
from auth.db import get_all_users

def get_authenticator():
    users = get_all_users()

    credentials = {"usernames": {}}

    for username, name, password in users:
        credentials["usernames"][username] = {
            "name": name,
            "email": f"{username}@app.com",  
            "password": password
        }

    authenticator = stauth.Authenticate(
        credentials,
        cookie_name="auth_cookie",
        key="Secret_key",
        cookie_expiry_days=30
    )

    return authenticator