import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
EMBEDDINGS_PATH = os.path.join(ROOT_PATH, 'vector_embeddings')
QUESTIONS_FILE_PATH = os.path.join(ROOT_PATH, 'questions.txt')

# FAISS_DATABASE_NAME = 'vector_index'
# FAISS_DATABASE_EXTENSION = '.faiss'

@dataclass
class FaissDatabaseParameters():
    FAISS_DATABASE_NAME: str = 'vector_index'
    FAISS_DATABASE_EXTENSION: str = '.faiss'

@dataclass
class AdminUserParameters():
    username: str = os.getenv('ADMIN_USERNAME')
    password: str = os.getenv('ADMIN_PASSWORD')
    email: str = os.getenv('ADMIN_EMAIL')
    role: str = os.getenv('ADMIN_ROLE')

