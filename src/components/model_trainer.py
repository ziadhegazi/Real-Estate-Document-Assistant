"""
In here we load the data andtrain the model
"""

import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from typing import List
from src.exception import CustomException

# A simple logger for the file
from src.logger import get_logger
logger = get_logger(__name__)

# Define the model name for the embeddings
MODEL_NAME = "all-MiniLM-L6-v2"

def setup_vector_store(chunks: List[Document], persist_directory: str) -> Chroma:
    """
    Creates a ChromaDB vector store from document chunks.

    Args:
        chunks: A list of Document objects (chunks).
        persist_directory: The directory to save the ChromaDB database.

    Returns:
        A ChromaDB vector store object.
    """
    try:
        # Create an embedding function
        embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        
        # Create and persist the vector store
        vector_store = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=persist_directory
        )
        vector_store.persist()
        logger.info(f"Vector store created and saved to '{persist_directory}'.")
        return vector_store
    except Exception as e:
        raise CustomException(e, sys) from e

def load_vector_store(persist_directory: str) -> Chroma:
    """
    Loads an existing ChromaDB vector store.

    Args:
        persist_directory: The directory where the ChromaDB database is saved.

    Returns:
        A ChromaDB vector store object.
    """
    try:
        # Create an embedding function
        embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        
        # Load the existing vector store
        vector_store = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
        logger.info(f"Vector store loaded from '{persist_directory}'.")
        return vector_store
    except Exception as e:
        raise CustomException(e, sys) from e

if __name__ == '__main__':
    # Example usage for testing the module
    from src.components.data_ingestion import load_documents_from_pdf
    from src.components.data_transformation import chunk_documents
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    sample_pdf_path = os.path.join(project_root, 'data', 'sample.pdf')
    persist_dir = os.path.join(project_root, 'db')
    
    # Run the full process for demonstration
    try:
        if os.path.exists(sample_pdf_path):
            documents = load_documents_from_pdf(sample_pdf_path)
            chunks = chunk_documents(documents)
            vector_store = setup_vector_store(chunks, persist_dir)
            loaded_vector_store = load_vector_store(persist_dir)
    except CustomException as e:
        logger.error(f"Error during model training: {e}")