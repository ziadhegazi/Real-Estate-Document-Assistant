import os
from src.components.model_trainer import load_vector_store
from src.logger import get_logger
from langchain.docstore.document import Document
from typing import List, Tuple

logger = get_logger(__name__)

def get_rag_response(query: str, vector_store) -> Tuple[str, List[Document]]:
    """
    Performs a retrieval-augmented generation query.

    Args:
        query: The user's question.
        vector_store: The ChromaDB vector store.

    Returns:
        A tuple containing the LLM's response and the retrieved source documents.
    """
    try:
        # Step 1: Retrieve relevant documents (chunks)
        retrieved_docs = vector_store.similarity_search(query, k=4)
        
        # Step 2: Format the retrieved documents as context for the LLM
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents for the query.")
        
        # The actual LLM call will be handled by the Flask application,
        # which will combine the context and the query.
        return context, retrieved_docs
        
    except Exception as e:
        logger.error(f"An error occurred during prediction: {e}")
        return "An error occurred while processing your request.", []

if __name__ == "__main__":
    # This section is for independent testing of the retrieval part
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    persist_dir = os.path.join(project_root, 'db')

    if not os.path.exists(persist_dir):
        logger.error(f"Vector store not found at '{persist_dir}'. Please run 'train_pipeline.py' first.")
    else:
        vector_store = load_vector_store(persist_dir)
        test_query = "What is the zoning for a single-family home?"
        context, docs = get_rag_response(test_query, vector_store)
        print("\n--- Retrieved Context ---")
        print(context[:500] + "...")
        print("\n--- Source Documents ---")
        for doc in docs:
            print(f"Source: {doc.metadata.get('source')}, Page: {doc.metadata.get('page')}")