from dotenv import load_dotenv
from enum import Enum, StrEnum
from pathlib import Path

load_dotenv()

import os

LLM = None
EMBEDDING_MODEL = None
VEC_DB = None
SQL_DB_CONN = None

BUILD_SCHEMA_QUERIES: list[str] = [
    """
    CREATE TABLE pdf(
        id INT PRIMARY KEY,
        title TEXT
    );
    """, 

    """
    CREATE TABLE pdf_splits(
        id INT PRIMARY KEY,
        pdf_id INT FOREIGN KEY
    )
    """
]

class Paths(Enum):
    DATA = Path(r"../data/raw/")
    SQL_DB = Path(r"../data/database.db")
    VEC_DB = Path(r"../data/vec/")

class ApiKeys(StrEnum):
    GROQ = os.environ["GROQ_API_KEY"]
    GOOGLE_GENAI = os.environ["GOOGLE_GENAI_KEY"]
    
class SqlQueries(StrEnum):
    pass


