import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.vector_store_manager import VectorStoreManager
from utils.chat_manager import ChatManager
from utils.qa_system import QASystem
from config import config

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    return {
        'doc_processor': DocumentProcessor(config.CHUNK_SIZE, config.CHUNK_OVERLAP),
        'vector_manager': VectorStoreManager(),
        'chat_manager': ChatManager(),
        'qa_system': QASystem()
    }

components = init_components()

# Initialize session state
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'current_doc_id' not in st.session_state:
    st.session_state.current_doc_id = None

def render_sidebar():
    """Render sidebar with chat history."""
    with st.sidebar:
        st.title("📚 Research Q&A")
        
        # New Chat button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.current_session_id = None
            st.session_state.current_doc_id = None
            st.rerun()
        
        st.divider()
        
        # Chat history
        st.subheader("Chat History")
        sessions = components['chat_manager'].get_all_sessions()
        
        if not sessions:
            st.write("No previous chats")
        else:
            for session in sessions:
                # Create a container for each chat item
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.button(
                            session.title,
                            key=f"session_{session.session_id}",
                            use_container_width=True,
                            help=f"Document: {session.document_name}"
                        ):
                            st.session_state.current_session_id = session.session_id
                            st.session_state.current_doc_id = session.doc_id
                            st.rerun()
                    
                    with col2:
                        if st.button(
                            "🗑️",
                            key=f"delete_{session.session_id}",
                            help="Delete chat",
                            use_container_width=True
                        ):
                            components['chat_manager'].delete_session(session.session_id)
                            if st.session_state.current_session_id == session.session_id:
                                st.session_state.current_session_id = None
                                st.session_state.current_doc_id = None
                            st.rerun()

def render_file_upload():
    """Render file upload interface."""
    st.header("📄 Upload Research Paper")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a research paper in PDF format"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            # Process document
            documents, doc_id = components['doc_processor'].load_and_split_pdf(uploaded_file)
            
            # Create or load vector store
            vector_store = components['vector_manager'].get_or_create_vector_store(documents, doc_id)
            
            # Create new chat session
            session_id = components['chat_manager'].create_session(uploaded_file.name, doc_id)
            
            # Update session state
            st.session_state.current_session_id = session_id
            st.session_state.current_doc_id = doc_id
            
            st.success(f"✅ Document processed successfully! ({len(documents)} chunks created)")
            st.rerun()

def render_chat_interface():
    """Render chat interface."""
    current_session = components['chat_manager'].get_session(st.session_state.current_session_id)
    
    if current_session is None:
        st.error("Session not found!")
        return
    
    st.header(f"💬 Chat: {current_session.document_name}")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in current_session.messages:
            with st.chat_message(message.role):
                st.write(message.content)
    
    # Chat input
    if question := st.chat_input("Ask a question about the research paper..."):
        # Add user message
        components['chat_manager'].add_message(st.session_state.current_session_id, "user", question)
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                vector_store = components['vector_manager'].load_vector_store(st.session_state.current_doc_id)
                
                if vector_store is None:
                    st.error("Vector store not found. Please re-upload the document.")
                    return
                
                result = components['qa_system'].ask_question(question, vector_store)
                answer = result['answer']
                sources = result['sources']
                
                st.write(answer)
                
                if sources:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(sources, 1):
                            st.write(f"**Source {i}:**")
                            st.write(source.page_content[:300] + "..." if len(source.page_content) > 300 else source.page_content)
                            st.write(f"*Page: {source.metadata.get('page', 'Unknown')}*")
                            st.divider()
        
        # Add assistant message
        components['chat_manager'].add_message(st.session_state.current_session_id, "assistant", answer)
        st.rerun()

def main():
    """Main application function."""
    render_sidebar()
    
    # Main content area
    if st.session_state.current_session_id is None:
        # Show file upload
        render_file_upload()
        
        # Show instructions
        st.markdown("""
        ## 🚀 Getting Started
        
        1. **Upload a PDF research paper** using the file uploader above
        2. **Ask questions** about the paper content
        3. **View chat history** in the sidebar
        4. **Start new chats** for different papers
        
        ## 📋 Features
        
        - **Smart chunking** of research papers for better context
        - **Vector similarity search** for relevant content retrieval
        - **Persistent chat history** across sessions
        - **Source citations** for transparency
        - **Reusable document processing** - documents are processed once and reused
        
        ## 🛠️ Requirements
        
        Make sure you have:
        - Ollama server running locally
        - Required Python packages installed
        - Sufficient disk space for vector stores
        """)
    
    else:
        # Show chat interface
        render_chat_interface()

if __name__ == "__main__":
    main()
    