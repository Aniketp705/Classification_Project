import streamlit as st
import time

from database.user import add_user, verify_user, create_user_table

# Ensure the user table exists when the app starts or this module is loaded
create_user_table()

def my_account():
    # Inject custom CSS for theme consistency
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main app container background */
    div[data-testid="stAppViewContainer"] {
        background-color: #222831 !important; /* Deep charcoal background */
        color: #e0e0e0; /* Default text color for the app view container */
    }

    /* Specific styling for the content block of the "Account" page */
    .main .block-container {
        background-color: #393e46 !important; /* Slightly lighter dark grey for the content card */
        padding: 40px !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
        margin-top: 30px !important;
        margin-bottom: 30px !important;
        max-width: 700px; /* Constrain width for account forms */
        margin-left: auto;
        margin-right: auto;
    }

    /* Titles */
    h1 {
        color: #00ADB5 !important; /* Bright Teal for the main title */
        font-weight: 700 !important;
        font-size: 2.8em !important;
        text-align: center;
        margin-bottom: 40px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Subheaders */
    h2, .st-emotion-cache-nahz7x h3 { /* Target h2, and h3 for subheader in Streamlit's markdown */
        color: #EEEEEE !important; /* Lighter white for subheaders */
        font-weight: 600 !important;
        font-size: 1.8em !important;
        margin-top: 30px !important;
        margin-bottom: 15px !important;
        border-bottom: 2px solid #00ADB5; /* Teal underline */
        padding-bottom: 5px;
    }

    /* Paragraph text */
    p {
        color: #cccccc !important; /* Light grey for body text */
        font-size: 1.1em !important;
        line-height: 1.7 !important;
        margin-bottom: 15px !important;
    }

    /* Text Inputs (Username, Password) */
    .stTextInput > label {
        color: #EEEEEE !important; /* Label color consistent with subheaders */
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        background-color: #444b54 !important; /* Darker grey for input background */
        color: #ffffff !important; /* White text color for input */
        border: 1px solid #5a626a !important;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ADB5 !important; /* Accent color on focus */
        box-shadow: 0 0 5px rgba(0, 173, 181, 0.5) !important;
    }

    /* Forms (st.form) - background for form elements */
    .st-emotion-cache-cnjsjv { /* This is a common class for st.form content container */
        background-color: #393e46; /* Match the main card background if needed, or slightly darker */
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444b54;
    }


    /* Buttons (Login, Register, Logout) */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #00ADB5 !important; /* Bright Teal for buttons */
        color: #ffffff !important;
        padding: 6px 20px !important; /* Adjusted vertical padding for normal height */
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 15px !important; /* Adjusted font size slightly */
        margin: 15px auto 10px auto; /* Adjust margin to prevent overlap */
        cursor: pointer;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        width: auto; /* Allow button to size to content */
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #009A9F !important; /* Greenish-blue on hover */
        color: #222831 !important; /* Dark text on lighter hover background */
        transform: translateY(-2px);
    }
    .stButton, .stFormSubmitButton {
        text-align: center; /* Center the buttons */
    }

    /* Radio buttons (Login/Register choice) */
    div[data-testid="stRadio"] > label > div { /* Target the label of the radio group */
        color: #EEEEEE !important; /* White color for radio group label */
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        background-color: #444b54; /* Darker background for the radio button container */
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    div[data-testid="stRadio"] label { /* Individual radio button labels */
        color: #cccccc !important; /* Light grey for radio button text */
    }
    div[data-testid="stRadio"] input[type="radio"]:checked + div { /* Checked radio button visual */
        background-color: #00ADB5 !important; /* Accent color when selected */
        border-color: #00ADB5 !important;
    }
    div[data-testid="stRadio"] input[type="radio"]:checked + div span {
        color: #ffffff !important; /* White text for selected radio button */
    }

    /* Info/Success/Error messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        font-weight: 500;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .stSuccess > div {
        background-color: #388e3c !important; /* Dark green background */
        color: #e8f5e9 !important; /* Very light green text */
        border-color: #4caf50 !important;
    }
    .stError > div {
        background-color: #d32f2f !important; /* Dark red background */
        color: #ffebee !important; /* Very light red text */
        border-color: #f44336 !important;
    }
    .stWarning > div {
        background-color: #fbc02d !important; /* Darker yellow background */
        color: #212121 !important; /* Dark text */
        border-color: #ffeb3b !important;
    }
    .stInfo > div {
        background-color: #00ADB5 !important; /* Teal info background */
        color: #ffffff !important; /* White text */
        border-color: #76D7C4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("👤 Account Management")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if st.session_state.logged_in:
        st.subheader(f"Welcome, {st.session_state.username}!")
        st.write("You are currently logged in.")
        if st.button("Logout"):
            with st.spinner("Logging out..."):
                time.sleep(1)
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("You have been logged out.")
            time.sleep(1)
            st.rerun()

    else:
        # Using columns for radio buttons for better visual separation
        login_col, register_col = st.columns(2)

        with login_col:
            if st.button("Login", key="main_login_btn"):
                st.session_state.form_choice = "Login"
        with register_col:
            if st.button("Register", key="main_register_btn"):
                st.session_state.form_choice = "Register"

        # Initialize form_choice if not set
        if "form_choice" not in st.session_state:
            st.session_state.form_choice = "Login" # Default to Login

        # Display forms based on session state choice
        if st.session_state.form_choice == "Login":
            st.subheader("Login to Your Account")
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")
                login_button = st.form_submit_button("Login")

                if login_button:
                    if not login_username or not login_password:
                        st.warning("Please enter both username and password.")
                    else:
                        if verify_user(login_username, login_password):
                            with st.spinner("Logging in..."):
                                time.sleep(1)
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.success(f"Welcome back, {login_username}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")

        elif st.session_state.form_choice == "Register":
            st.subheader("Create a New Account")
            with st.form("register_form"):
                reg_username = st.text_input("Choose a Username", key="reg_user")
                reg_password = st.text_input("Choose a Password", type="password", key="reg_pass")
                reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
                register_button = st.form_submit_button("Register")

                if register_button:
                    if not reg_username or not reg_password or not reg_password_confirm:
                        st.warning("Please fill in all fields.")
                    elif reg_password != reg_password_confirm:
                        st.error("Passwords do not match.")
                    else:
                        # Basic password strength check (example)
                        if len(reg_password) < 6:
                            st.warning("Password should be at least 6 characters long.")
                        elif add_user(reg_username, reg_password):
                            with st.spinner("Creating account..."):
                                time.sleep(1)
                            st.success(f"Account created successfully for {reg_username}! You can now login.")
                            st.session_state.form_choice = "Login" # Switch to Login tab after successful registration
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to create account. The username might already be taken.")
