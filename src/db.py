import config as cfg

from uuid import uuid4
from pathlib import Path
from datetime import datetime as dt 
import time
from typing import Any

from langchain_community.document_loaders import PyPDFLoader

class _Doc:
    def __init__(self, document: Path) -> None:
        self.id = str(uuid4())
        self.name = document.stem
        self.last_mod_date = (dt.fromtimestamp(document.stat().st_mtime)).isoformat(sep=" ", timespec="seconds")
        self.path = document

class _Split:
    def __init__(self, doc_id: str, content: Any) -> None:
        self.id = str(uuid4())
        self.doc_id = doc_id
        self.content = content

def _retrieve_doc_id(document_name: str) -> str:
    document_id = None

    with cfg.SQL_DB_CONN as conn:
        document_id = conn.execute(cfg.SqlQueries.RETRIEVE_DOC, (document_name))

    return document_id

def _retrieve_splits_ids(document_id: str) -> list[str]:
    splits_ids = None

    with cfg.SQL_DB_CONN as conn:
        cur = conn.execute(cfg.SqlQueries.RETRIEVE_SPLITS.value, (document_id))
        splits_ids = cur.fetchall() # I should check whether this is a single value tuple or not
    
    return splits_ids
       
def _delete_splits(document_id: str) -> None:
    with cfg.SQL_DB_CONN as conn:
        conn.execute(cfg.SqlQueries.REMOVE_DOC.value, (document_id))

def _delete_document(document_id: str) -> None:
    with cfg.SQL_DB_CONN as conn:
        conn.execute(cfg.SqlQueries.REMOVE_DOC.value, (document_id))

def _delete_vec_splits(splits_ids: list[str]) -> None:
    cfg.VEC_DB.remove(ids=splits_ids)

def _load_documents(document: _Doc) -> Any:
    loader = PyPDFLoader(document.path)
    return loader.load()

def _split_docs(document_id: str, loaded_docs: Any) -> list[_Split]: 
    splits = cfg.SPLITTER.split_documents(loaded_docs)
    return [_Split(document_id, split) for split in splits]

def _insert_doc(document: _Doc) -> None:
    with cfg.SQL_DB_CONN as conn:
        doc_tuple = (document.id, document.name, document.last_mod_date)
        conn.execute(cfg.SqlQueries.ADD_DOC.value, doc_tuple) 

def _insert_splits(splits: list[_Split]) -> None:
    with cfg.SQL_DB_CONN as conn:  
        for split in splits:
            split_tuple = (split.id, split.doc_id)
            conn.execute(cfg.SqlQueries.ADD_SPLITS.value, split_tuple)

def _insert_vec_db(splits: list[_Split]) -> None:
    for split in splits:
        cfg.VEC_DB.add_documents(documents=[split.content], ids=[split.id])
        time.sleep(4)

def add_document(document: Path):
    doc_ = _Doc(document)
    loaded_docs = _load_documents(doc_)
    splits = _split_docs(doc_.id, loaded_docs)
    _insert_splits(splits)
    _insert_vec_db(splits)

    cfg.SQL_DB_CONN.commit()

def remove_document(document: Path):
    doc_id = None
    splits_ids = None 

    doc_id = _retrieve_doc_id(document.stem)
    splits_ids = _retrieve_splits_ids(doc_id)
    _delete_splits(doc_id)
    _delete_document(doc_id)
    _delete_vec_splits(splits_ids)

    cfg.SQL_DB_CONN.commit()


