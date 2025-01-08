import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import constants
import utils
from faiss_db import FaissDB
from streamlit_chat import message as st_message
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from sqlite_db import SQLite
import pandas as pd

load_dotenv()

faiss_db = FaissDB(constants.FaissDatabaseParameters().FAISS_DATABASE_NAME, utils.load_embeddings_model())

def get_chain(vectorstore_data, chat_llm):
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_llm,
        retriever=vectorstore_data,
        memory=memory,
        )
    return conversation_chain

def handle_userinput(query, results):
    st.session_state.history = []
    response = {}
    if results:
        response = st.session_state.conversation({'question': query})
        if response['answer'] != "I don't know":
            st.session_state.chat_history = response['chat_history']
            st.session_state.history.append({"message": query, "is_user": True})
            st.session_state.history.append({"message": response['answer'], "is_user": False})
        else:
            st.session_state.history.append({"message": query, "is_user": True})
            st.session_state.history.append({"message": "Sorry. I am unable to answer the question.", "is_user": False})            
    else:
        st.session_state.history.append({"message": query, "is_user": True})
        st.session_state.history.append({"message": "Sorry. I am unable to answer the question.", "is_user": False})
    with st.container(border=True):
        for i, message in enumerate(st.session_state.history):
            (st_message(**message, key=str(i)))
    return response

def app(SQLiteDB:SQLite):
    query = ""
    if st.session_state.login_status:
        results = None
        col1, col2 = st.columns([0.9, 0.6])
        with col1.container(border=True):
            if "conversation" not in st.session_state:
                st.session_state.conversation = None
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = None
            vector_embdddings = faiss_db.reteive_vectorstore()
            if vector_embdddings is None:
                st.error('No Embeddings Found.. Please upload documents and do embeddings calculation..')
            else:
                scrollbar_css = """
                <style>
                /* Customize the scroll bar */
                ::-webkit-scrollbar {
                    width: 12px;
                }

                ::-webkit-scrollbar-track {
                    background: #f1f1f1;
                }

                ::-webkit-scrollbar-thumb {
                    background: #888;
                    border-radius: 10px;
                }

                ::-webkit-scrollbar-thumb:hover {
                    background: #555;
                }
                </style>
                """
                st.markdown(scrollbar_css, unsafe_allow_html=True)
                if vector_embdddings:
                    query = st.text_input('**Ask a prompt about your :orange[documents]**')
                    st.markdown('---')
                    if query:
                        with st.spinner("Processing your prompt... Please wait..."):
                            retriever = vector_embdddings.as_retriever(search_type="similarity_score_threshold", \
                                                                                search_kwargs={"k": 3,"score_threshold": 0.3})
                            try:
                                results=retriever.invoke(query)
                                if results:
                                    st.session_state.conversation = get_chain(retriever,utils.load_chat_model())
                            except:
                                results = []
                            response = handle_userinput(query, results)
    else:
        st.error('User is not logged in..')