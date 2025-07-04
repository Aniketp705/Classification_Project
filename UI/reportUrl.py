import streamlit as st
import time # Import time for the spinner
import driver
import driver.reporter # Ensure this import is present to access the report_url function


def app():
    # Inject custom CSS for theme consistency
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
        }

        /* Keyframe for a subtle fade-in animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Main app container background */
        div[data-testid="stAppViewContainer"] {
            background-color: #222831 !important; /* Deep charcoal background */
            color: #e0e0e0; /* Default text color for the app view container */
        }

        /* Specific styling for the content block of the page */
        .main .block-container {
            background-color: #393e46 !important; /* Slightly lighter dark grey for the content card */
            padding: 40px !important;
            border-radius: 15px !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
            margin-top: 30px !important;
            margin-bottom: 30px !important;
            max-width: 700px; /* Constrain width for forms */
            margin-left: auto;
            margin-right: auto;
            /* Animation for the main content block */
            animation: fadeIn 0.8s ease-out forwards;
        }

        /* Titles */
        h1 {
            color: #009A9F !important; /* Darker Teal for the main title */
            font-weight: 700 !important;
            font-size: 2.8em !important;
            text-align: center;
            margin-bottom: 40px !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            opacity: 0; /* Start invisible for animation */
            animation: fadeIn 0.8s ease-out 0.2s forwards; /* Delayed fade-in */
        }

        /* Subheaders (if used, e.g., for sections within the page) */
        h2 { /* Not explicitly used on this page for main content, but good to keep consistent */
            color: #EEEEEE !important; /* Lighter white for subheaders */
            font-weight: 600 !important;
            font-size: 1.8em !important;
            margin-top: 30px !important;
            margin-bottom: 15px !important;
            border-bottom: 2px solid #009A9F; /* Darker Teal underline */
            padding-bottom: 5px;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.4s forwards;
        }

        /* Paragraph text (for st.write) */
        p {
            color: #cccccc !important; /* Light grey for body text */
            font-size: 1.1em !important;
            line-height: 1.7 !important;
            margin-bottom: 15px !important;
            text-align: center; /* Center the descriptive text */
            opacity: 0; /* Start invisible for animation */
            animation: fadeIn 0.8s ease-out 0.4s forwards; /* Delayed fade-in */
        }

        /* Text Input field */
        .stTextInput > label {
            color: #EEEEEE !important; /* Label color consistent with subheaders */
            font-weight: bold;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.6s forwards; /* Delayed fade-in */
        }
        .stTextInput > div > div > input {
            background-color: #444b54 !important; /* Darker grey for input background */
            color: #ffffff !important; /* White text color for input */
            border: 1px solid #5a626a !important;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            opacity: 0; /* Start invisible for animation */
            animation: fadeIn 0.8s ease-out 0.7s forwards; /* Further delayed fade-in */
        }
        .stTextInput > div > div > input:focus {
            border-color: #009A9F !important; /* Accent color on focus */
            box-shadow: 0 0 5px rgba(0, 154, 159, 0.5) !important; /* Adjusted shadow color */
        }

        /* Button Styling */
        .stButton > button {
            background-color: #009A9F !important; /* Darker Teal for buttons */
            color: #ffffff !important;
            padding: 12px 25px; /* Standard button padding */
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px;
            margin: 20px auto;
            cursor: pointer;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            width: auto;
            opacity: 0; /* Start invisible for animation */
            animation: fadeIn 0.8s ease-out 0.8s forwards; /* Further delayed fade-in */
        }
        .stButton > button:hover {
            background-color: #00ADB5 !important; /* Lighter teal on hover */
            color: #222831 !important; /* Dark text on lighter hover background */
            transform: translateY(-2px);
        }
        .stButton {
            text-align: center; /* Center the button */
        }

        /* Alert Messages (Success, Error, Warning) */
        .stAlert {
            border-radius: 8px;
            padding: 15px;
            font-weight: 500;
            margin-top: 15px;
            margin-bottom: 15px;
            opacity: 0; /* Start invisible for animation */
            animation: fadeIn 0.8s ease-out 0.9s forwards; /* Delayed fade-in */
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
        .stInfo > div { /* If st.info is used */
            background-color: #009A9F !important; /* Darker Teal info background */
            color: #ffffff !important; /* White text */
            border-color: #00ADB5 !important; /* Lighter Teal border */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Report URL")
    
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # Message for non-logged-in users, also animated
        st.markdown(
            """
            <p style="opacity: 0; animation: fadeIn 0.8s ease-out 0.4s forwards; text-align: center;">
                You must be logged in to report a URL.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.error("You must be logged in to report a URL.") # Keeping Streamlit's native error for clarity
        return
    else:
        st.write("Use this form to report a URL that you believe is unsafe or phishing-related.")

        url_to_report = st.text_input("Enter the URL to report:", placeholder="https://example.com", label_visibility="hidden")

        if st.button("Report URL"):
            if url_to_report:
                with st.spinner("Reporting URL..."):
                    # The time.sleep here is a simulation.
                    # In a deployed app, remove this if driver.reporter.report_url takes real time.
                    time.sleep(1.5)
                    try:
                        status, message = driver.reporter.report_url(url_to_report)
                        
                        if status:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred during the reporting process: {e}")
            else:
                st.warning("Please enter a valid URL to report.")
