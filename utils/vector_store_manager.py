import os
import pickle
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_stores = {}
    
    def get_vector_store_path(self, doc_id: str) -> str:
        """Get the path for storing vector store files."""
        return os.path.join(config.VECTOR_STORE_DIR, doc_id)
    
    def vector_store_exists(self, doc_id: str) -> bool:
        """Check if vector store exists for given document ID."""
        path = self.get_vector_store_path(doc_id)
        return os.path.exists(f"{path}.faiss") and os.path.exists(f"{path}.pkl")
    
    def create_vector_store(self, documents: List[Document], doc_id: str) -> FAISS:
        """Create and save vector store from documents."""
        vector_store = FAISS.from_documents(documents, self.embeddings)
        
        # Save vector store
        path = self.get_vector_store_path(doc_id)
        vector_store.save_local(config.VECTOR_STORE_DIR, doc_id)
        
        # Cache in memory
        self.vector_stores[doc_id] = vector_store
        
        return vector_store
    
    def load_vector_store(self, doc_id: str) -> Optional[FAISS]:
        """Load existing vector store."""
        if doc_id in self.vector_stores:
            return self.vector_stores[doc_id]
        
        if self.vector_store_exists(doc_id):
            try:
                vector_store = FAISS.load_local(
                    config.VECTOR_STORE_DIR, 
                    self.embeddings,
                    doc_id
                )
                self.vector_stores[doc_id] = vector_store
                return vector_store
            except Exception as e:
                print(f"Error loading vector store: {e}")
                return None
        
        return None
    
    def get_or_create_vector_store(self, documents: List[Document], doc_id: str) -> FAISS:
        """Get existing vector store or create new one."""
        vector_store = self.load_vector_store(doc_id)
        if vector_store is None:
            vector_store = self.create_vector_store(documents, doc_id)
        return vector_store
    