"""
Handling the data and transforming it
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.docstore.document import Document

# A simple logger for the file
from src.logger import get_logger
logger = get_logger(__name__)

def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Splits a list of documents into smaller, overlapping chunks.

    Args:
        documents: A list of Document objects to be chunked.
        chunk_size: The desired size of each chunk.
        chunk_overlap: The number of characters to overlap between chunks.

    Returns:
        A list of Document objects representing the chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logger.error(f"An error occurred during document chunking: {e}")
        raise

if __name__ == '__main__':
    # Example usage for testing the module independently
    from src.components.data_ingestion import load_documents_from_pdf
    import os
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    sample_pdf_path = os.path.join(project_root, 'data', 'sample.pdf')

    try:
        # Load the documents (e.g., from a dummy PDF)
        if os.path.exists(sample_pdf_path):
            documents = load_documents_from_pdf(sample_pdf_path)
            if documents:
                # Chunk the documents
                chunks = chunk_documents(documents)
                logger.info(f"First chunk content: {chunks[0].page_content[:200]}...")
            else:
                logger.warning("No documents to chunk. Please ensure the PDF is not empty.")
    except FileNotFoundError:
        pass # The error is already handled in data_ingestion