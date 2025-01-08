import os
from langchain_community.vectorstores import FAISS
import constants
import pandas as pd

class FaissDB():
    def __init__(self, index_name, embeddings):
        self.index_name = index_name
        self.embeddings = embeddings
        self.database_filepath = constants.EMBEDDINGS_PATH

    def reteive_vectorstore(self):
        if os.path.exists(self.database_filepath):
            vector_data = FAISS.load_local(folder_path=self.database_filepath,
                                           embeddings=self.embeddings,
                                           index_name=self.index_name,
                                           allow_dangerous_deserialization=True)
            return vector_data
        else:
            return None
        
    def update_vectorstore(self, vector_data, vector_data_chunk):
        vector_data.merge_from(vector_data_chunk)
        return vector_data
    
    def show_vector_data(self):
        store = self.reteive_vectorstore()
        vector_store_dict = store.docstore._dict
        data_row = []
        for key in vector_store_dict.keys():
            page_content = vector_store_dict[key].page_content
            title = vector_store_dict[key].metadata['title']
            data_row.append({'chunk_id':key, 'title':title, 'content':page_content})
        data_frame = pd.DataFrame(data_row)
        return data_frame
    
    def delete_vectorstore(self, vector_data, document_names):
        for document_name in document_names:
            document_name_list = document_name.split('.')       ## Install_python.pdf -> Install_python
            extension = document_name_list[1].split('_')[0]
            updated_document_name = document_name_list[0] + '.' + extension
            data_frame = self.show_vector_data()
            chunks_list = data_frame.loc[data_frame['document']==updated_document_name]['chunk_id'].tolist()
            vector_data.delete(chunks_list)
        return vector_data
    
    def create_vectorstore(self, text_chunks):
        vector_data = FAISS.from_texts(text_chunks, self.embeddings)
        return vector_data
    
    def save_vectorstore(self, vector_data):
        vector_data.save_local(self.database_filepath, self.index_name)