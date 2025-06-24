import streamlit as st

def show_about():
    st.markdown("""
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

    /* Keyframe for a border slide-in animation on subheaders */
    @keyframes slideInBorder {
        from { width: 0; }
        to { width: 100%; }
    }

    /* Main app container background */
    div[data-testid="stAppViewContainer"] {
        background-color: #222831 !important; /* Deep charcoal background */
        color: #e0e0e0; /* Default text color for the app view container */
    }

    /* Specific styling for the content block of the "About" page */
    .main .block-container {
        background-color: #393e46 !important; /* Slightly lighter dark grey for the content card */
        padding: 40px !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important; /* More pronounced shadow */
        margin-top: 30px !important;
        margin-bottom: 30px !important;
        max-width: 900px; /* Constrain width for better readability on wide screens */
        margin-left: auto; /* Center the block */
        margin-right: auto; /* Center the block */
        /* Animation for the main content block */
        animation: fadeIn 0.8s ease-out forwards;
    }


    /* Titles */
    h1 {
        color: #00ADB5 !important; /* Bright Teal for the main title, stands out */
        font-weight: 700 !important;
        font-size: 2.8em !important;
        text-align: center;
        margin-bottom: 40px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Subtle text shadow */
        opacity: 0; /* Start invisible for animation */
        animation: fadeIn 0.8s ease-out 0.2s forwards; /* Delayed fade-in */
    }

    /* Subheaders */
    h2 {
        color: #EEEEEE !important; /* Lighter white for subheaders */
        font-weight: 600 !important;
        font-size: 1.8em !important;
        margin-top: 30px !important;
        margin-bottom: 15px !important;
        border-bottom: 2px solid #00ADB5; /* Teal underline for visual separation */
        padding-bottom: 5px;
        opacity: 0; /* Start invisible for animation */
        animation: fadeIn 0.8s ease-out 0.4s forwards; /* Further delayed fade-in */
        position: relative; /* Needed for pseudo-element underline animation */
    }

    /* Animated underline for subheaders (optional, subtle) */
    h2::after {
        content: '';
        position: absolute;
        bottom: -2px; /* Position it slightly below the text */
        left: 0;
        width: 100%;
        height: 2px;
        background-color: #00ADB5; /* Teal color */
        transform: scaleX(0); /* Start hidden */
        transform-origin: bottom left;
        transition: transform 0.4s ease-out; /* Smooth transition */
    }
    h2:hover::after {
        transform: scaleX(1); /* Expand on hover */
    }


    /* Paragraph text */
    p {
        color: #cccccc !important; /* Light grey for body text, good contrast on dark background */
        font-size: 1.1em !important;
        line-height: 1.7 !important; /* Improved line spacing for readability */
        margin-bottom: 15px !important;
        opacity: 0; /* Start invisible for animation */
        animation: fadeIn 0.8s ease-out 0.6s forwards; /* Even further delayed fade-in */
    }

    /* List items inside markdown */
    ul {
        list-style-type: disc;
        padding-left: 25px; /* Indent lists */
        color: #cccccc; /* List item text color */
    }
    li {
        margin-bottom: 8px; /* Spacing between list items */
        color: #cccccc;
        opacity: 0; /* Start invisible for animation */
        animation: fadeIn 0.8s ease-out 0.8s forwards; /* Delayed fade-in for list items */
    }

    /* Links */
    a {
        color: #76D7C4 !important; /* A contrasting greenish-blue for links */
        text-decoration: none !important; /* Remove default underline */
        font-weight: 500 !important;
        transition: color 0.3s ease, transform 0.3s ease !important; /* Smooth transition for color and transform */
    }

    a:hover {
        color: #00ADB5 !important; /* Change to main title color on hover */
        text-decoration: underline !important; /* Add underline on hover */
        transform: translateY(-2px); /* Slight lift on hover */
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("About Phishing Detector")
    st.markdown("""
    ## What is Phishing?
    Phishing is a type of cyber attack where attackers impersonate legitimate organizations to steal sensitive information such as usernames, passwords, and credit card details.

    ## How Does This App Work?
    This app uses machine learning algorithms to analyze URLs and detect potential phishing attempts. It provides users with a simple interface to check the safety of links.

    ## Features
    - URL analysis for phishing detection
    - User account management
    - Secure login and registration

    ## Contact
    For any questions or feedback, please contact us at [Gmail](mailto:aniket22217pawar@gmail.com)
    """)
    st.markdown("""
    ## Acknowledgements
    - This app is built using [Streamlit](https://streamlit.io/), a powerful framework for building data applications.
    - The machine learning model is trained on a dataset of known phishing and legitimate URLs.
    """)