from dotenv import load_dotenv
from enum import Enum, StrEnum
from pathlib import Path

load_dotenv()

import os

LLM = None
EMBEDDING_MODEL = None
VEC_DB = None

class Paths(Enum):
    DATA: Path = Path(r"../data/raw/")
    SQL_DB: Path = Path(r"../data/database.db")
    VEC_DB: Path = Path(r"../data/vec/")

class ApiKeys(StrEnum):
    GROQ: str = os.environ(GROQ_API_KEY)   
    GOOGLE_GENAI: str = os.environ(GOOGLE_GENAI_KEY)
    
class SqlQueries(StrEnum):
    pass


