# **Real Estate RAG Assistant**

This project is a Retrieval-Augmented Generation (RAG) assistant designed to answer questions about real estate documents. It demonstrates a complete RAG pipeline from data ingestion to a user-friendly web interface.

## **Features**

* **Document Ingestion:** Processes PDF files to build a knowledge base.  
* **Vector Indexing:** Uses sentence-transformers for embeddings and ChromaDB for vector storage.  
* **Retrieval:** Retrieves relevant document chunks based on semantic similarity.  
* **Generation:** Utilizes a Large Language Model (LLM) to generate a grounded response.  
* **Web Interface:** A simple, interactive chat application built with Flask and Tailwind CSS.

## **Getting Started**

### **Prerequisites**

* Python 3.8+  
* A Gemini API key

### **Setup**

1. **Clone the repository:**  
   '''
   git clone \<your-repo-url\>  
   cd real-estate-rag-project
   '''

3. **Set up a virtual environment:**
   '''
   conda create -n real_estate_env python=3.10 
   conda activate real_estate_env
   '''

5. **Install dependencies:**
   '''
   pip install \-r requirements.txt
   '''

7. Add your Gemini API Key:
   '''
   Create a .env file in the root directory and add your API key.  
   GEMINI\_API\_KEY="your-gemini-api-key-here"
   '''

9. Add your data:  
   Create a folder named data in the root directory and place a PDF file named sample.pdf inside it. This will be the document your assistant learns from.  
10. Build the knowledge base:  
   Run the training pipeline to process the documents and create the vector store.
   ''' 
   python src/pipeline/train\_pipeline.py
   '''

   This will create a db folder containing the vector database.  
11. **Run the web application:**  
   '''
   python application.py
   '''

   The application will be available at http://127.0.0.1:5000.

## **Project Structure**

.  
├── artifacts/  
├── data/  
│   └── sample.pdf  
├── notebook/  
├── src/  
│   ├── components/  
│   │   ├── data\_ingestion.py  
│   │   ├── data\_transformation.py  
│   │   ├── model\_trainer.py  
│   │   ├── ...  
│   ├── pipeline/  
│   │   ├── train\_pipeline.py  
│   │   ├── predict\_pipeline.py  
│   │   └── ...  
│   ├── logger.py  
│   ├── exception.py  
│   └── utils.py  
├── templates/  
│   └── index.html  
├── .gitignore  
├── application.py  
├── requirements.txt  
├── README.md  
└── setup.py  
