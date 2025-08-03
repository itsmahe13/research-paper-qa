# 📚 Research Paper Q&A System

A comprehensive AI-powered research paper analysis tool that allows users to upload PDF research papers and ask questions about their content. Built with Streamlit, LangChain, FAISS, and Ollama for local LLM processing.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-v0.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 📖 **Document Processing**
- **PDF Upload & Processing**: Automatic chunking with configurable overlap
- **Smart Caching**: Documents processed once and reused across sessions
- **Vector Storage**: FAISS-based similarity search for relevant content retrieval

### 💬 **Chat Interface**
- **ChatGPT-like Sidebar**: Clean, intuitive chat history management
- **Persistent Sessions**: All conversations saved and resumable
- **Multi-Document Support**: Switch between different research papers
- **Source Citations**: Transparent answers with document references

### 🤖 **AI Integration**
- **Local LLM**: Powered by Ollama (privacy-focused, offline processing)
- **Contextual Answers**: Retrieval-augmented generation (RAG) for accurate responses
- **Customizable Models**: Support for various Ollama models

## 🏗️ Project Structure

```
research-paper-qa/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration management
├── requirements.txt                 # Python dependencies
├── utils/
│   ├── document_processor.py       # PDF processing and chunking
│   ├── vector_store_manager.py     # FAISS vector store management
│   ├── chat_manager.py             # Chat history and sessions
│   └── qa_system.py                # Q&A chain with Ollama
├── vector_stores/                  # Cached vector databases
├── chat_history/                   # Persistent chat sessions
└── README.md                       # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsmahe13/research-paper-qa.git
   cd research-paper-qa
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama server
   ollama serve
   
   # Pull a model (in another terminal)
   ollama pull llama2
   # or ollama pull mistral
   # or ollama pull codellama
   ```

4. **Configure the application**
   
   Edit `config.py` to match your setup:
   ```python
   OLLAMA_MODEL = "llama2"  # Change to your preferred model
   OLLAMA_BASE_URL = "http://localhost:11434"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📋 Usage Guide

### 1. **Upload Research Paper**
- Click on the file uploader
- Select a PDF research paper
- Wait for processing (first-time only)

### 2. **Ask Questions**
- Type questions in the chat input
- Get AI-powered answers with source citations
- View relevant document excerpts

### 3. **Manage Chat History**
- **New Chat**: Start fresh with a new document
- **Resume**: Click on previous chats in sidebar
- **Delete**: Remove unwanted chat sessions

### 4. **Example Questions**
- "What is the main hypothesis of this paper?"
- "What methodology was used in the experiments?"
- "What are the key findings and conclusions?"
- "How does this work compare to previous research?"

## ⚙️ Configuration

### Model Configuration
```python
# config.py
OLLAMA_MODEL = "llama2"           # Available: llama2, mistral, codellama, etc.
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Document Processing
```python
CHUNK_SIZE = 1000                 # Size of text chunks
CHUNK_OVERLAP = 200              # Overlap between chunks
```

### Chat Settings
```python
MAX_CHAT_HISTORY = 50            # Maximum chat sessions to keep
```

## 🛠️ Advanced Features

### Custom Prompt Templates
Modify the QA prompt in `utils/qa_system.py`:
```python
self.prompt_template = PromptTemplate(
    template="""Your custom prompt here...""",
    input_variables=["context", "question"]
)
```

### Vector Store Optimization
Adjust embedding model in `utils/vector_store_manager.py`:
```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   ```

2. **Model Not Found**
   ```bash
   # List available models
   ollama list
   
   # Pull required model
   ollama pull llama2
   ```

3. **Memory Issues**
   - Reduce `CHUNK_SIZE` in config.py
   - Use smaller embedding models
   - Limit concurrent sessions

4. **PDF Processing Errors**
   - Ensure PDF is not corrupted
   - Check file permissions
   - Try different PDF files

## 📊 Performance Tips

- **Document Caching**: Processed documents are automatically cached
- **Model Selection**: Smaller models (7B) are faster but less accurate
- **Chunk Optimization**: Balance chunk size vs. context relevance
- **Hardware**: More RAM allows larger models and better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug mode
streamlit run app.py --logger.level=debug
```

## 📈 Roadmap

- [ ] **Multi-format Support**: Word documents, text files
- [ ] **Advanced Analytics**: Document comparison, topic modeling
- [ ] **Export Features**: Chat export, summary generation
- [ ] **API Integration**: REST API for programmatic access
- [ ] **Docker Support**: Containerized deployment
- [ ] **Cloud Models**: OpenAI, Anthropic API integration

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://langchain.com/) - LLM application framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [FAISS](https://faiss.ai/) - Vector similarity search
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/itsmahe13/research-paper-qa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/itsmahe13/research-paper-qa/discussions)
- **Email**: itsmahendran13@gmail.com

---

⭐ **Star this repo** if you find it helpful!
