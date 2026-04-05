from dotenv import load_dotenv
from enum import Enum, StrEnum
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

import os

LLM = None
EMBEDDING_MODEL = None
VEC_DB = None
SQL_DB_CONN = None

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1_000,
    chunk_overlap=200,
    add_start_index=True
)

BUILD_SCHEMA_QUERIES: list[str] = [
    """
    CREATE TABLE document(
        id INT PRIMARY KEY,
        title TEXT
    );
    """, 

    """
    CREATE TABLE splits(
        id INT PRIMARY KEY,
        doc_id INT FOREIGN KEY
    )
    """
]

class Paths(Enum):
    DATA = Path(r"../data/raw/")
    SQL_DB = Path(r"../data/database.db")
    VEC_DB = Path(r"../data/vec/")

class ApiKeys(StrEnum):
    GROQ = os.environ["GROQ_API_KEY"]
    GOOGLE_GENAI = os.environ["GOOGLE_API_KEY"]
    
class SqlQueries(StrEnum):
    ADD_DOC = """
        INSERT INTO document VALUES (?, ?, ?);
    """

    REMOVE_DOC = """
        REMOVE FROM document WHERE id = ?;
        """

    ADD_SPLITS = """
        INSERT INTO doc_splits VALUES (?, ?);
    """

    REMOVE_SPLITS = """
        REMOVE FROM doc_splits WHERE doc_id = ?;
    """

    RETRIEVE_DOC = """
        SELECT id FROM document WHERE title = ?; 
    """

    RETRIEVE_SPLITS = """
        SELECT id FROM doc_splits WHERE doc_id = ?;
    """









