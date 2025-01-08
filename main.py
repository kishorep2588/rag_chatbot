import streamlit as st
from streamlit_option_menu import option_menu
import constants
import embeddings, chatbot, login, register, user_settings
from sqlite_db import SQLite
import time

st.set_page_config('Chatbot', layout='wide')

SQLiteDB = SQLite('user_db.sqlite3')

## declaring session state parameters
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "login_status" not in st.session_state:
    st.session_state.login_status = False
if "user_status" not in st.session_state:
    st.session_state.user_status = False
if "user_register_role" not in st.session_state:
    st.session_state.user_register_role = ""

users = SQLiteDB.fetch_users()

if users is not None:
    st.session_state.user_status = True
else:
    admin_user = constants.AdminUserParameters()
    SQLiteDB.create_user(admin_user.username, admin_user.password, admin_user.email, admin_user.role)

def get_options():
    if st.session_state.user_status and st.session_state.user_register_role == 'admin':
        options = ['Login', 'Upload Documents', 'Chatbot', 'Settings']
        icons = ['person-circle', 'database', 'robot', 'person-lines-fill']
    else:
        options = ['Login', 'Upload Documents', 'Chatbot', 'Settings', 'Register']
        icons = ['person-circle', 'database', 'robot', 'person-lines-fill', 'person-fill-add']
    return options, icons

def change_states():
    placeholder = st.empty()
    placeholder.info(f"User - {st.session_state.username} Logged out")
    time.sleep(5)
    placeholder.empty()
    st.session_state.login_status = False
    st.session_state.role = ""
    st.session_state.username = ""
    st.session_state.text_username = ""
    st.session_state.text_role = ""


with st.sidebar:
    options, icons = get_options()
    option_selected = option_menu(
        menu_title=None,
        options=options,
        menu_icon=None,
        icons = icons,
        styles={
                    "container": {"padding": "0!important", "background-color": "#34495E"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {
                        "font-size": "20px",
                        "font-family": "system-ui",
                        "text-align": "left",
                        "margin": "5px",
                        "font-weight": "bold",
                        "--hover-color": "#E74C3C"
                    },
                    "nav-link-selected": {"background-color": "#28B463"}
                }
    )

with st.container():
    col1,col2 = st.columns([0.05, 0.95])
    with col1:
        st.image("./images/chatbot1.png", width=100)
    with col2:
        st.markdown("<h1 style='text-align: center; color: orange;'>RAG Based Chatbot</h1>", unsafe_allow_html=True)
    
    #st.markdown("<h1 style='text-align: center; color: orange;'>RAG Based Chatbot</h1>", unsafe_allow_html=True)
st.markdown('---')

if option_selected == 'Login':
    login.app(SQLiteDB)

elif option_selected == "Upload Documents":
    embeddings.app()

elif option_selected == "Chatbot":
    chatbot.app(SQLiteDB)

elif option_selected == "Settings":
    user_settings.app(SQLiteDB)

elif option_selected == "Register":
    register.app(SQLiteDB)

if st.session_state.login_status:
    with st.sidebar:
        st.markdown('---')
        col1, _, col2 = st.columns([0.3, 0.2, 0.5])
        with col1:
            logout = st.button(label='Logout', on_click=change_states)
        with col2:
            with st.container(border=True):
                st.text_input(label="Username", value=st.session_state.username, key='text_username')
                st.text_input(label='Role', value=st.session_state.role, key="text_role")



