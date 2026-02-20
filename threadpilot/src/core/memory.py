from __future__ import annotations

from pathlib import Path
from typing import List

try:
    import chromadb
except Exception:
    chromadb = None


class MemoryStore:
    def __init__(self, persist_dir: Path, collection_name: str = "project_context") -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._collection = None

        if chromadb is not None:
            client = chromadb.PersistentClient(path=str(self.persist_dir))
            self._collection = client.get_or_create_collection(name=collection_name)

    def add_context(self, key: str, text: str) -> None:
        if self._collection is None:
            return
        self._collection.upsert(documents=[text], ids=[key])

    def search(self, query: str, limit: int = 3) -> List[str]:
        if self._collection is None:
            return []
        results = self._collection.query(query_texts=[query], n_results=limit)
        docs = results.get("documents") or [[]]
        return docs[0]
