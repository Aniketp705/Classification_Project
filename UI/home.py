import streamlit as st
import pandas as pd
import numpy as np
import pickle, time, re, socket, requests
import whois, tldextract
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to extract features from a URL (Original logic preserved)
def extract_features(url):
    feature_dict = {
    'NumDots': 0, 'SubdomainLevel': 0, 'PathLevel': 0, 'UrlLength': 0,
    'NumDash': 0, 'NumDashInHostname': 0, 'AtSymbol': 0, 'TildeSymbol': 0,
    'NumUnderscore': 0, 'NumPercent': 0, 'NumQueryComponents': 0, 'NumAmpersand': 0,
    'NumHash': 0, 'NumNumericChars': 0, 'NoHttps': 0, 'RandomString': 0,
    'IpAddress': 0, 'DomainInSubdomains': 0, 'DomainInPaths': 0, 'HostnameLength': 0,
    'PathLength': 0, 'QueryLength': 0, 'DoubleSlashInPath': 0, 'NumSensitiveWords': 0,
    'EmbeddedBrandName': 0, 'PctExtHyperlinks': 0, 'PctExtResourceUrls': 0, 'ExtFavicon': 0,
    'InsecureForms': 0, 'RelativeFormAction': 0, 'ExtFormAction': 0, 'AbnormalFormAction': 0,
    'PctNullSelfRedirectHyperlinks': 0, 'FrequentDomainNameMismatch': 0, 'FakeLinkInStatusBar': 0,
    'RightClickDisabled': 0, 'PopUpWindow': 0, 'SubmitInfoToEmail': 0, 'IframeOrFrame': 0,
    'MissingTitle': 0, 'ImagesOnlyInForm': 0, 'SubdomainLevelRT': 0, 'UrlLengthRT': 0,
    'PctExtResourceUrlsRT': 0, 'AbnormalExtFormActionR': 0, 'ExtMetaScriptLinkRT': 0,
    'PctExtNullSelfRedirectHyperlinksRT': 0
    }

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        path = parsed.path or ''
        query = parsed.query or ''
        ext = tldextract.extract(url)
        domain = ext.domain + '.' + ext.suffix if ext.suffix else ext.domain

        # Basic URL features
        feature_dict['NumDots'] = url.count('.')
        feature_dict['SubdomainLevel'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
        feature_dict['PathLevel'] = len([p for p in path.split('/') if p])
        feature_dict['UrlLength'] = len(url)
        feature_dict['NumDash'] = url.count('-')
        feature_dict['NumDashInHostname'] = hostname.count('-') if hostname else 0
        feature_dict['AtSymbol'] = url.count('@')
        feature_dict['TildeSymbol'] = url.count('~')
        feature_dict['NumUnderscore'] = url.count('_')
        feature_dict['NumPercent'] = url.count('%')
        feature_dict['NumQueryComponents'] = len(query.split('&')) if query else 0
        feature_dict['NumAmpersand'] = url.count('&')
        feature_dict['NumHash'] = url.count('#')
        feature_dict['NumNumericChars'] = len(re.findall(r'\d', url))
        feature_dict['NoHttps'] = int(parsed.scheme != 'https')
        feature_dict['DoubleSlashInPath'] = int('//' in path)
        feature_dict['HostnameLength'] = len(hostname)
        feature_dict['PathLength'] = len(path)
        feature_dict['QueryLength'] = len(query)

        # Check if domain is an IP address
        try:
            socket.inet_aton(hostname)
            feature_dict['IpAddress'] = 1
        except:
            feature_dict['IpAddress'] = 0

        # WHOIS information (simplified for demonstration, actual WHOIS might take time)
        try:
            whois_info = whois.whois(domain)
            # Add simple checks based on WHOIS data if needed
            feature_dict['DomainInSubdomains'] = int(domain in ext.subdomain)
            feature_dict['DomainInPaths'] = int(domain in path)
        except Exception as e:
            # print(f"WHOIS lookup failed for {domain}: {e}")
            feature_dict['DomainInSubdomains'] = 0
            feature_dict['DomainInPaths'] = 0


        # Content-based features (requires fetching the page, can be slow/fail)
        try:
            response = requests.get(url, timeout=5) 
            response.raise_for_status() 
            soup = BeautifulSoup(response.content, 'html.parser')

            # Sensitive words
            sensitive_words = ['secure', 'account', 'webscr', 'login', 'ebayisapi', 'signin', 'banking']
            feature_dict['NumSensitiveWords'] = sum(word in url.lower() for word in sensitive_words)

            # Embedded brand name (example: 'paypal')
            feature_dict['EmbeddedBrandName'] = int('paypal' in url.lower())

            # External resources (simplified calculation)
            total_links = soup.find_all('a')
            external_links = [link for link in total_links if link.get('href') and urlparse(link.get('href')).netloc != hostname] # Compare hostnames
            feature_dict['PctExtHyperlinks'] = len(external_links) / len(total_links) if total_links else 0

            total_resources = soup.find_all(['img', 'script', 'link'])
            external_resources = [res for res in total_resources if res.get('src') and urlparse(res.get('src')).netloc != hostname] # Compare hostnames
            feature_dict['PctExtResourceUrls'] = len(external_resources) / len(total_resources) if total_resources else 0

            # Favicon
            favicon = soup.find('link', rel='shortcut icon') or soup.find('link', rel='icon')
            if favicon and favicon.get('href'):
                favicon_url = urlparse(favicon.get('href'))
                if favicon_url.netloc and favicon_url.netloc != hostname:
                    feature_dict['ExtFavicon'] = 1


            # Forms
            forms = soup.find_all('form')
            for form in forms:
                action = form.get('action')
                if action:
                    parsed_action = urlparse(action)
                    if parsed_action.scheme in ['http', 'https'] and parsed_action.netloc and parsed_action.netloc != hostname:
                        feature_dict['ExtFormAction'] = 1
                    elif not parsed_action.scheme and not parsed_action.netloc: # Relative URL
                        feature_dict['RelativeFormAction'] = 1
                    else: # No action attribute
                        feature_dict['AbnormalFormAction'] = 1


            # Iframe
            iframes = soup.find_all('iframe')
            feature_dict['IframeOrFrame'] = int(bool(iframes))

            # Title
            title = soup.title.string if soup.title else ''
            feature_dict['MissingTitle'] = int(title is None or title.strip() == '') # Check for None explicitly

            # Images only in form (This logic might need refinement depending on exact definition)
            # Currently checks if there are no images on the page but there are forms.
            images = soup.find_all('img')
            feature_dict['ImagesOnlyInForm'] = int(len(images) == 0 and len(forms) > 0)


        except requests.exceptions.RequestException as e:
            # Handle network/request errors gracefully
            # print(f"Error fetching content for {url}: {e}")
            pass # Keep default values

        except Exception as e:
            # Handle other potential errors during content parsing
            # print(f"Error parsing content for {url}: {e}")
            pass # Keep default values


    except Exception as e:
        # Catch any errors during initial URL parsing or other steps
        print(f"Error processing URL: {e}")
        # The feature_dict was initialized with default values, so we can just return it.


    return feature_dict # Ensure the dictionary is always returned


# get the weights and bias from the pickle file
try:
    with open('Models/model_parameters.pkl', 'rb') as file:
        w, b = pickle.load(file)
except FileNotFoundError:
    st.error("Error: 'model_parameters.pkl' not found. Please make sure the model file is in the correct directory.")
    st.stop() # Stop the app if the model file is missing
except Exception as e:
    st.error(f"Error loading model parameters: {e}")
    st.stop()


# sigmoid function for binary classification
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Function to apply the UI styling for the predict page
def _apply_predict_ui_style():
    # This function is now removed, and its content is inlined into 'predict()'
    # to ensure the CSS is injected and animations are applied correctly.
    pass

def predict():
    # Set the page title and icon
    try:
        st.set_page_config(page_title="Phishing URL Detector", layout="wide", initial_sidebar_state="collapsed")
    except:
        pass

    # --- INJECT CUSTOM CSS FOR STYLING AND ANIMATIONS ---
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

        /* Main app container background (for the entire Streamlit page) */
        div[data-testid="stAppViewContainer"] {
            background-color: #222831 !important; /* Deep charcoal background */
            color: #e0e0e0; /* Default text color for the app view container */
        }

        /* Specific styling for the content block of the page */
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
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.4s forwards;
        }

        /* Paragraph text (for st.markdown description) */
        p {
            color: #cccccc !important; /* Light grey for body text, good contrast on dark background */
            font-size: 1.1em !important;
            line-height: 1.7 !important; /* Improved line spacing for readability */
            margin-bottom: 15px !important;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.4s forwards;
        }

        /* List items inside markdown - NOT USED IN PREDICT PAGE BUT GOOD TO KEEP */
        ul {
            list-style-type: disc;
            padding-left: 25px;
            color: #cccccc;
        }
        li {
            margin-bottom: 8px;
            color: #cccccc;
        }

        /* Links - NOT USED IN PREDICT PAGE BUT GOOD TO KEEP */
        a {
            color: #76D7C4 !important;
            text-decoration: none !important;
            font-weight: 500 !important;
            transition: color 0.3s ease, text-decoration 0.3s ease !important;
        }

        a:hover {
            color: #00ADB5 !important;
            text-decoration: underline !important;
        }

        /* Specific styling for the predict page elements */

        /* Style for the text input field */
        .stTextInput > label {
            color: #EEEEEE !important; /* Label color consistent with h2 */
            font-weight: bold;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.6s forwards; /* Delayed fade-in */
        }
        .stTextInput > div > div > input {
            background-color: #444b54 !important; /* Darker grey for input background */
            color: #ffffff !important; /* White text color for input */
            border: 1px solid #5a626a !important; /* Border consistent with dark theme */
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.7s forwards; /* Further delayed fade-in */
        }
        .stTextInput > div > div > input:focus {
            border-color: #00ADB5 !important; /* Highlight color on focus */
            box-shadow: 0 0 5px rgba(0, 173, 181, 0.5) !important;
        }


        /* Style for the analyze button */
        .stButton > button {
            background-color: #00ADB5 !important; /* Bright Teal for the button */
            color: #ffffff !important; /* Force text color to white */
            padding: 12px 25px;
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
            width: auto; /* Allow button to size to content */
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.8s forwards; /* Further delayed fade-in */
        }
        .stButton > button:hover {
            background-color: #009A9F !important; /* Greenish-blue on hover */
            color: #222831 !important; /* Dark text on lighter hover background */
            transform: translateY(-2px);
        }
        .stButton {
            text-align: center;
        }


        /* Styling for the result messages */
        /* Custom classes for HTML messages to mimic Streamlit's alerts but allow HTML */
        .custom-alert {
            border-radius: 8px;
            padding: 15px;
            font-weight: 500;
            margin-top: 15px;
            margin-bottom: 15px;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.9s forwards; /* Delayed fade-in */
            word-wrap: break-word; /* Ensure long URLs wrap */
            white-space: normal; /* Ensure normal white-space behavior */
        }
        .custom-alert.success {
            background-color: #388e3c; /* Dark green background */
            color: #e8f5e9; /* Very light green text */
            border: 1px solid #4caf50;
        }
        .custom-alert.error {
            background-color: #d32f2f; /* Dark red background */
            color: #ffebee; /* Very light red text */
            border: 1px solid #f44336;
        }
        .custom-alert.info { /* For st.info like messages */
            background-color: #009A9F; /* Darker Teal info background */
            color: #ffffff; /* White text */
            border: 1px solid #00ADB5; /* Lighter Teal border */
        }


        /* Styling for the metric */
        .stMetric {
            background-color: #444b54 !important; /* Dark background for metric */
            padding: 15px;
            border-radius: 8px;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
            text-align: center;
            opacity: 0;
            animation: fadeIn 0.8s ease-out 0.9s forwards; /* Delayed fade-in */
        }
        .stMetric label {
            color: #00ADB5 !important; /* Label color accent */
            font-size: 1em;
            font-weight: bold;
        }
        .stMetric div[data-testid="stMetricValue"] {
            color: #ffffff !important; /* Value color white */
            font-size: 1.8em;
            font-weight: bold;
        }


        /* Styling for the expander */
        /* Note: Streamlit's internal class names for expanders can be brittle,
                 these selectors are based on common structures. Adjust if needed. */
        .st-emotion-cache-lky0z6 > div > div { /* Target expander header */
            background-color: #444b54 !important; /* Darker background for header */
            color: #ffffff !important; /* White text */
            border-radius: 8px !important;
            padding: 10px;
            margin-bottom: 0 !important; /* Remove bottom margin from header */
            border: 1px solid #5a626a !important; /* Subtle border */
            opacity: 0;
            animation: fadeIn 0.8s ease-out 1.0s forwards; /* Delayed fade-in */
        }
        .st-emotion-cache-lky0z6 .st-emotion-cache-10trjem { /* Target expander title text */
            color: #EEEEEE !important; /* Lighter white for title */
            font-weight: bold;
        }
        .st-emotion-cache-1k7hjsq { /* Target expander content body */
            background-color: #2a3a4a !important; /* Slightly lighter than app background, darker than card */
            padding: 10px;
            border-bottom-left-radius: 8px !important; /* Rounded corners for content */
            border-bottom-right-radius: 8px !important;
            border: 1px solid #5a626a !important; /* Consistent border */
            margin-top: 0 !important; /* Remove top margin from content */
            opacity: 0;
            animation: fadeIn 0.8s ease-out 1.1s forwards; /* Delayed fade-in for expander content */
        }


        /* Styling for the dataframe within the expander */
        .stDataFrame {
            border: none !important;
        }
        .stDataFrame .dataframe { /* Target the pandas dataframe table */
            background-color: #2a3a4a !important; /* Match expander content background */
            color: #ffffff !important; /* White text */
        }
        .stDataFrame .dataframe th { /* Table headers */
            background-color: #3a4a5a !important; /* Darker header background */
            color: #00ADB5 !important; /* Accent color for headers */
            font-weight: bold;
        }
        .stDataFrame .dataframe td { /* Table data cells */
            border-bottom: 1px solid #3a4a5a !important; /* Subtle border between rows */
        }


        /* Styling for the footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9em;
            color: #cccccc; /* Lighter grey text */
            opacity: 0;
            animation: fadeIn 0.8s ease-out 1.2s forwards; /* Delayed fade-in */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # --- END CUSTOM CSS INJECTION ---

    st.title("🔍 Phishing Website Detector")
    # Apply fade-in to the markdown description - NOW USING <b> TAGS FOR BOLDING
    st.markdown("""
    <p style="opacity: 0; animation: fadeIn 0.8s ease-out 0.4s forwards; text-align: center;">
    Enter a URL to check whether it might be <b>malicious</b> or <b>safe</b> using a custom Logistic Regression model.
    </p>
    """, unsafe_allow_html=True)


    url = st.text_input("🔗 Enter a URL:", placeholder="https://example.com", label_visibility="hidden")
    button = st.button("Analyze URL")

    col1, col2 = st.columns([2, 1])

    if button:
        if url:
            with st.spinner("Analyzing URL and extracting features..."):
                time.sleep(2)

                if not urlparse(url).scheme:
                    url = "https://" + url
                    st.info(f"Assuming HTTPS scheme: {url}")

                features = extract_features(url)
                input_vector = np.array(list(features.values())).reshape(1, -1)

                if input_vector.shape[1] != w.shape[0]:
                    st.error(f"Feature mismatch: Extracted {input_vector.shape[1]} features, but model expects {w.shape[0]}. Please check the feature extraction logic and model file.")
                    return

                z = np.dot(input_vector, w) + b
                probability = sigmoid(z)
                prediction = 1 if probability >= 0.5 else 0

            with col1:
                st.subheader("🔎 Result")
                if prediction == 1:
                    # Using custom-alert with 'error' class and <b> tag for bolding within HTML
                    st.markdown(f'<div class="custom-alert error">⚠️ The URL `{url}` is likely to be <b>malicious</b>.</div>', unsafe_allow_html=True)
                else:
                    # Using custom-alert with 'success' class and <b> tag for bolding within HTML
                    st.markdown(f'<div class="custom-alert success">✅ The URL `{url}` is likely to be <b>safe</b>.</div>', unsafe_allow_html=True)

            with col2:
                st.subheader("📊 Confidence")
                st.metric(label="Probability of being Malicious", value=f"{float(probability * 100):.2f} %", delta=None)

            st.markdown("---")

            with st.expander("🛠 View Extracted Features"):
                features_df = pd.DataFrame.from_dict(features, orient='index', columns=['Value'])
                st.dataframe(features_df)

        else:
            st.error("🚫 Please enter a valid URL before analyzing.")

    st.markdown(
        """
        <br>
        <div class="footer">
            <p>Developed as a demonstration for phishing URL detection.</p>
            <p>&copy; 2023-2025 PhishingDetector. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
