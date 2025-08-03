from typing import List, Optional
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from config import config

class QASystem:
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=0.1
        )
        
        self.prompt_template = PromptTemplate(
            template="""You are a helpful research assistant. Use the following context from the research paper to answer the question. 
            If you cannot find the answer in the context, say so clearly.
            
            Context: {context}
            
            Question: {question}
            
            Answer: """,
            input_variables=["context", "question"]
        )
    
    def create_qa_chain(self, vector_store):
        """Create QA chain with vector store."""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
    
    def ask_question(self, question: str, vector_store) -> dict:
        """Ask question and get answer with sources."""
        qa_chain = self.create_qa_chain(vector_store)
        result = qa_chain.invoke({"query": question})
        
        return {
            "answer": result["result"],
            "sources": result.get("source_documents", [])
        }
