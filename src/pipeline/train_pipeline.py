import os
import sys
from src.components.data_ingestion import load_documents_from_pdf
from src.components.data_transformation import chunk_documents
from src.components.model_trainer import setup_vector_store
from src.exception import CustomException
from src.logger import get_logger
from dotenv import load_dotenv

logger = get_logger(__name__)

def train_pipeline(pdf_path: str):
    """
    An end-to-end pipeline to ingest, chunk, and index real estate documents.

    Args:
        pdf_path: The path to the PDF file to be processed.
    """
    try:
        logger.info("Starting the training pipeline.")
        
        # Step 1: Load documents
        documents = load_documents_from_pdf(pdf_path)
        
        if not documents:
            logger.warning("No documents loaded. Aborting pipeline.")
            return
            
        # Step 2: Split documents into chunks
        chunks = chunk_documents(documents)
        
        # Step 3: Set up and persist the vector store
        # This will create a 'db' folder at the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..')
        persist_dir = os.path.join(project_root, 'db')
        
        vector_store = setup_vector_store(chunks, persist_dir)
        
        logger.info("Training pipeline completed successfully.")
    except Exception as e:
        raise CustomException(e, sys) from e
    
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Example usage:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    # Assuming the PDF is in a 'data' folder at the project root
    sample_pdf = os.path.join(project_root, 'data', 'sample.pdf')
    
    if not os.path.exists(sample_pdf):
        logger.error(f"Please create a 'data' folder and place a PDF file named 'sample.pdf' inside it. Path: {sample_pdf}")
    else:
        try:
            train_pipeline(sample_pdf)
        except CustomException as e:
            logger.error(f"Error running training pipeline: {e}")