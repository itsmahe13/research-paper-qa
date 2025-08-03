import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"  # Change to your preferred model
    
    # Vector Store Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    VECTOR_STORE_DIR: str = "vector_stores"
    
    # Chat Configuration
    CHAT_HISTORY_DIR: str = "chat_history"
    MAX_CHAT_HISTORY: int = 10
    
    # UI Configuration
    PAGE_TITLE: str = "Research Paper Q&A Assistant"
    PAGE_ICON: str = "📚"

config = Config()

# Ensure directories exist
os.makedirs(config.VECTOR_STORE_DIR, exist_ok=True)
os.makedirs(config.CHAT_HISTORY_DIR, exist_ok=True)