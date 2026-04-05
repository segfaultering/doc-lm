import doc_lm.config as cfg

import sqlite3

from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


def _init_llm():
    return ChatGroq(
        model="qwen/qwen3.5-32b",
        api_key=cfg.ApiKeys.GROQ.value
    )

def _init_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=cfg.ApiKeys.GOOGLE_GENAI.value
    )
        
def _init_vec_db():
    return Chroma(
        embedding_function=cfg.EMBEDDING_MODEL,
        persist_directory=cfg.Paths.VEC_DB.value
    )

def _init_sql_db():
    cfg.SQL_DB_CONN = sqlite3.connect(cfg.Paths.SQL_DB.value)    
    with cfg.SQL_DB_CONN as conn:
        for query in cfg.BUILD_SCHEMA_QUERIES:
            conn.execute(query)

    cfg.SQL_DB_CONN.commit()

def setup() -> None:
    cfg.LLM = _init_llm()
    cfg.EMBEDDING_MODEL = _init_embedding_model()
    cfg.SQL_DB_CONN = _init_sql_db()
    cfg.VEC_DB = _init_vec_db()

if __name__ == "__main__":
    setup()
