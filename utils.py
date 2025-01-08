import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings , GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_embeddings_model():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv('GOOGLE_API_KEY'))


def load_chat_model():
    return GoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.1)


def chunk_texts(texts):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', ' ', ''],
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len
    )
    text_chunks = text_splitter.split_text(texts)
    return text_chunks

def update_prompt_data(SQLiteDB, prompt, results, response):
    query_data = SQLiteDB.fetch_queries()
    prompts = []
    if query_data is not None:
        for _, query_response in enumerate(query_data):
            prompts.append(query_response[0])
        if prompt not in prompts and len(prompts) > 0:
            prompts.insert(0, prompt)
        updated_prompt_info = [prompt for _, prompt in enumerate(prompts)]
    else:
        updated_prompt_info = [prompt]
    SQLiteDB.update_queries(updated_prompt_info)

def view_prompts(SQLiteDB):
    query_data = SQLiteDB.fetch_queries()
    if query_data is not None:
        query_dict = {
            'id': [number+1 for number in range(len(query_data))],
            'Prompt': [query_info[0] for query_info in query_data],
        }
        return query_dict
    return None

def clean_and_combine_documents(documents):
    cleaned_documents = []
    for document in documents:
        content = document['page_content']
        content = content.replace('• ', '\n•')
        content = content.replace('  ', ' ')
        cleaned_documents.append(content.strip())
    return cleaned_documents


