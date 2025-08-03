import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from config import config

@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

@dataclass
class ChatSession:
    session_id: str
    document_name: str
    doc_id: str
    created_at: str
    messages: List[ChatMessage]
    title: str = ""

class ChatManager:
    def __init__(self):
        self.sessions = {}
        self.load_all_sessions()
    
    def generate_session_id(self) -> str:
        """Generate unique session ID."""
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    def get_session_file_path(self, session_id: str) -> str:
        """Get file path for session."""
        return os.path.join(config.CHAT_HISTORY_DIR, f"{session_id}.json")
    
    def create_session(self, document_name: str, doc_id: str) -> str:
        """Create new chat session."""
        session_id = self.generate_session_id()
        session = ChatSession(
            session_id=session_id,
            document_name=document_name,
            doc_id=doc_id,
            created_at=datetime.now().isoformat(),
            messages=[],
            title=f"Chat about {document_name[:30]}..."
        )
        
        self.sessions[session_id] = session
        self.save_session(session_id)
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to session."""
        if session_id in self.sessions:
            message = ChatMessage(
                role=role,
                content=content,
                timestamp=datetime.now().isoformat()
            )
            self.sessions[session_id].messages.append(message)
            
            # Update title if it's the first user message
            if role == 'user' and len(self.sessions[session_id].messages) == 1:
                self.sessions[session_id].title = content[:50] + "..." if len(content) > 50 else content
            
            self.save_session(session_id)
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get session by ID."""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[ChatSession]:
        """Get all sessions sorted by creation date."""
        return sorted(self.sessions.values(), key=lambda x: x.created_at, reverse=True)
    
    def save_session(self, session_id: str):
        """Save session to file."""
        if session_id in self.sessions:
            file_path = self.get_session_file_path(session_id)
            with open(file_path, 'w') as f:
                json.dump(asdict(self.sessions[session_id]), f, indent=2)
    
    def load_session(self, session_id: str) -> Optional[ChatSession]:
        """Load session from file."""
        file_path = self.get_session_file_path(session_id)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Convert messages back to ChatMessage objects
                messages = [ChatMessage(**msg) for msg in data['messages']]
                data['messages'] = messages
                
                session = ChatSession(**data)
                self.sessions[session_id] = session
                return session
            except Exception as e:
                print(f"Error loading session {session_id}: {e}")
        return None
    
    def load_all_sessions(self):
        """Load all sessions from files."""
        if not os.path.exists(config.CHAT_HISTORY_DIR):
            return
        
        for filename in os.listdir(config.CHAT_HISTORY_DIR):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                self.load_session(session_id)
    
    def delete_session(self, session_id: str):
        """Delete session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        
        file_path = self.get_session_file_path(session_id)
        if os.path.exists(file_path):
            os.remove(file_path)