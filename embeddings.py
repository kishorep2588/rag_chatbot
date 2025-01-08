import os
import streamlit as st
import constants
import utils
from dotenv import load_dotenv
import PyPDF2
from faiss_db import FaissDB

load_dotenv()

faiss_db = FaissDB(constants.FaissDatabaseParameters().FAISS_DATABASE_NAME, utils.load_embeddings_model())


def app():
    if st.session_state.role == 'admin' or st.session_state.role == 'developer':
        uploaded_files = st.file_uploader('Upload Files', 
                                                    type=['pdf','docx','md','txt','pptx'], 
                                                    accept_multiple_files=True)
        if uploaded_files:
            text = ""
            for uploaded_file in uploaded_files:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()

            text_chunks = utils.chunk_texts(text)
            if st.button('Calculate Embeddings'):
                with st.spinner():
                    vector_store = faiss_db.create_vectorstore(text_chunks)
                    faiss_db.save_vectorstore(vector_data=vector_store)
                st.success('Embeddings have been calculated successfully..')
    else:
        st.error('User is not authorized')