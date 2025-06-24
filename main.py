import streamlit as st
from streamlit_option_menu import option_menu
from UI import home, account, about, reportUrl
import pathlib


#set page config
try:
    st.set_page_config(
        page_title="Phishing Detector",
        page_icon=":guardsman:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except:
    pass

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None


class MultiApp:
    def __init__(self):
        if st.session_state.logged_in:
            self.apps = [
                {"title": "Home", "function": home.predict},
                {"title": "Account", "function": account.my_account},
                {"title": "About", "function": about.show_about},
                {"title": "Report", "function": reportUrl.app}
            ]
        else:
            self.apps = [
                {"title": "Home", "function": home.predict},
                {"title": "Account", "function": account.my_account},
                {"title": "Report", "function": reportUrl.app}
            ]

    def run(self):

        # Inject custom CSS
        st.markdown(
            """
            <style>
            /* Target the outermost navbar wrapper with class 'menu' */
            [data-testid = "st.menu"] {
                background-color: transparent ; /* Or match your theme */
                border-radius: 30px !important;
                box-shadow: none !important;
                margin-top: 10px;
                padding: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        # only display the menu if the user is logged in
        if st.session_state.logged_in:
            menu_items = ["Home","Report", "About","Account"]
            icons_list = ["house","flag", "info-circle", "person"]
        
        else:
            menu_items = ["Home","Report", "Account"]
            icons_list = ["house","flag", "person"]

        selected = option_menu(
            menu_title=None,
            options=menu_items,
            icons=icons_list,
            orientation="horizontal",
            default_index=0,
            styles={
                "container": {
                    # "padding": "0", 
                    "background-color": "#1f1f2e",
                    "border-radius": "10px",
                },
                "nav-link": {
                    "font-size": "16px",
                    "color": "white",
                    "margin": "0",
                    "left": "0px",
                },
                "nav-link-selected": {
                    "color": "black",
                    "background-color": "#fce4ec",
                },
            }
        )



        for app in self.apps:
            if app["title"] == selected:
                app["function"]()

app = MultiApp()
app.run()
