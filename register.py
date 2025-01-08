import streamlit as st 
from streamlit_option_menu import option_menu
from sqlite_db import SQLite


def app(SQLiteDB:SQLite):
    if st.session_state.login_status and st.session_state.role != 'admin':
        st.error('User is not Authorized..')
    elif not st.session_state.login_status:
        message_string = '''
                        Please login with admin account to register any user.
                        Please click on Login if you are not admin to access the application
                        '''
        st.info(message_string)
    else:
        _, col2, _ = st.columns([0.25, 0.5, 0.25])
        with col2.container(border=True):
            options_selected = option_menu(
                            menu_title = None,
                            options=['Register'],
                            icons = ['person-fill-add'],
                            orientation='horizontal',
                            default_index=0,
                            styles={
                                        "container": {"padding": "0!important", "background-color": "#34495E"},
                                        "icon": {"color": "white", "font-size": "20px"},
                                        "nav-link": {
                                            "font-size": "20px",
                                            "font-family": "system-ui",
                                            "text-align": "center",
                                            "margin": "5px",
                                            "font-weight": "bold"
                                        },
                                        "nav-link-selected": {"background-color": "#28B463"}
                                    }        
                            ) 
            if options_selected == 'Register':
                with col2.form(key='Register', clear_on_submit=True):
                    username = st.text_input(label='Username')
                    password = st.text_input(label='Password')
                    email = st.text_input(label='Email')
                    role = st.selectbox(label='role', options=['user', 'admin', 'developer'])
                    register_button = st.form_submit_button(label='Register')
                    if register_button:
                        result = SQLiteDB.create_user(username, password, email, role)
                        if result is not None:
                            st.info(f'User - {result[0]} is successfully created with role - {result[3]}')
                            st.session_state.user_register_role = result[3]
                        else:
                            st.info(f'User - {username} is already exists in Datatbase')