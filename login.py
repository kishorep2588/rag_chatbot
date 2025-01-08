import os
import streamlit as st
from streamlit_option_menu import option_menu
from sqlite_db import SQLite


def app(SQLiteDB:SQLite):
    if not st.session_state.login_status:
        _, col2, _ = st.columns([0.25, 0.5, 0.25])
        with col2.container(border=True):
            options_selected = option_menu(
                            menu_title = None,
                            options=['Login'],
                            icons = ['person-fill-check'],
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
            if options_selected == 'Login':
                with col2.form(key='login', clear_on_submit=True):
                    username = st.text_input(label='Username')
                    password = st.text_input(label='Password')
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        result = SQLiteDB.authenticate_user(username, password)
                        if result is not None:
                            st.info(f'user - {result[0]} logged in Successfully with role - {result[3]}')
                            st.session_state.role = result[3]
                            st.session_state.username = result[0]
                            st.session_state.login_status = True
                        else:
                            st.error(f'No User Present in the Database..')
    else:
        st.error(f'User - {st.session_state.username} is already logged in..')



    