import os
import requests
import json
from flask import Flask, render_template, request, jsonify
from src.pipeline.predict_pipeline import get_rag_response
from src.components.model_trainer import load_vector_store
from src.logger import get_logger
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "")

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
logger = get_logger(__name__)

# Load the vector store once when the application starts
# This is an efficient way to avoid re-loading the database for every request
current_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(current_dir, 'db')
vector_store = None

def load_db():
    global vector_store
    try:
        vector_store = load_vector_store(persist_dir)
        logger.info("Vector store loaded successfully on app startup.")
    except Exception as e:
        logger.error(f"Failed to load vector store on startup: {e}")
        vector_store = None

# A thread to load the database without blocking the main app startup
# This is a good practice for larger projects
db_loader_thread = threading.Thread(target=load_db)
db_loader_thread.start()

# --- Gemini API Call Logic ---
def get_gemini_response(prompt: str) -> str:
    """
    Sends a request to the Gemini API and returns the text response.
    """
    if not API_KEY:
        logger.error("API_KEY environment variable is not set.")
        return "I'm sorry, the API key is not configured. Please contact the administrator."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "text/plain"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        
        result = response.json()
        
        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return text
        else:
            logger.error(f"Unexpected API response structure: {result}")
            return "I'm sorry, I couldn't generate a response. The LLM response was malformed."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Gemini API: {e}")
        return "I'm sorry, there was a problem communicating with the AI model. Please try again later."
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from API: {e}")
        return "I'm sorry, I couldn't understand the AI model's response."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return "I'm sorry, something went wrong. Please try again."

@app.route('/')
def home():
    """Renders the main chat interface page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles user queries and returns a RAG response."""
    if vector_store is None:
        return jsonify({"response": "The knowledge base is not yet ready. Please run 'train_pipeline.py' first and restart the app."})

    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"response": "Please enter a question."})

    try:
        # Get context from the vector store
        context, docs = get_rag_response(user_query, vector_store)
        
        # Craft a prompt for the LLM
        prompt = f"""
            You are a helpful real estate assistant. Use the following context to answer the user's question. 
            If the answer is not in the context, say "I'm sorry, I cannot answer this question based on the provided documents."
            Do not make up any information.
            
            Context:
            {context}
            
            User's question: {user_query}
            
            Answer:
        """
        
        # Get the final response from the LLM
        final_response = get_gemini_response(prompt)
        
        return jsonify({"response": final_response})
    
    except Exception as e:
        logger.error(f"An error occurred during chat processing: {e}")
        return jsonify({"response": "An internal server error occurred. Please check the logs."})

if __name__ == '__main__':
    # Check if the vector store exists before running the app
    if not os.path.exists(persist_dir):
        logger.warning(f"Vector store not found at '{persist_dir}'. Please run 'train_pipeline.py' to create it.")
        print("\n*** IMPORTANT ***")
        print("Please run `python src/pipeline/train_pipeline.py` to create the knowledge base before running the web server.")
        print("After it finishes, you can run `python application.py`.")
        exit()
    else:
        app.run(debug=True, port=5000)