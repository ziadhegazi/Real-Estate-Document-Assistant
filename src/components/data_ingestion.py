"""
Reading the data from a database/ file path
"""

import os
import sys
from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain.docstore.document import Document
from src.exception import CustomException

# A simple logger for the file
from src.logger import get_logger
logger = get_logger(__name__)

def load_documents_from_pdf(pdf_path: str) -> List[Document]:
    """
    Loads documents from a single PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        A list of Document objects, where each object represents a page in the PDF.
    """
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} pages from '{pdf_path}'.")
        return documents
    except Exception as e:
        raise CustomException(e, sys) from e

if __name__ == '__main__':
    # Example usage (assuming a 'data' folder with 'sample.pdf')
    # This part can be used for testing the module independently
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    sample_pdf_path = os.path.join(project_root, 'data', 'sample.pdf')

    # Create a dummy PDF for demonstration
    if not os.path.exists(sample_pdf_path):
        os.makedirs(os.path.dirname(sample_pdf_path), exist_ok=True)
        # You would need a real PDF here. This is a placeholder.
        logger.warning(f"Please place a PDF file at '{sample_pdf_path}' to run this example.")
    
    # Load the dummy documents
    try:
        loaded_docs = load_documents_from_pdf(sample_pdf_path)
        # Process the documents here if needed
        # For a full pipeline, you would pass these to the next step
    except CustomException as e:
        logger.error(f"Error during data ingestion: {e}")