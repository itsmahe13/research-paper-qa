import os
import hashlib
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
import tempfile

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def generate_doc_id(self, content: bytes) -> str:
        """Generate a unique ID for the document based on its content."""
        return hashlib.md5(content).hexdigest()
    
    def load_and_split_pdf(self, uploaded_file) -> tuple[List[Document], str]:
        """Load PDF and split into chunks, return documents and document ID."""
        # Read file content
        content = uploaded_file.read()
        doc_id = self.generate_doc_id(content)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Load PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
            
            # Split documents
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata['doc_id'] = doc_id
                chunk.metadata['source'] = uploaded_file.name
            
            return chunks, doc_id
        
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
