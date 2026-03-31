import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Load and index data 
@st.cache_resource(show_spinner=False)
def load_data(api_key): 
    if not api_key:
        return None
        
    with st.spinner(text="Indexing documentation... This uses a local embedding model (free & unlimited)."):
        
        # Set Embedding Model (Local)
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5",
            trust_remote_code=True
        )
    
        # Set LLM (Gemini)
        Settings.llm = Gemini(
            model="models/gemini-2.5-flash", 
            api_key=api_key
        )
        
        # Load documents
        try:
            # We add required_exts to ensure it doesn't try to read hidden folders or system files
            reader = SimpleDirectoryReader(
                input_dir='./data', 
                recursive=True, 
                required_exts=[".pdf"]
            )
            
            # Use filename_as_id to help the index keep track of different PDFs
            docs = reader.load_data()
            
            # DEBUG: This will print in your VS Code / Terminal console
            # Helps to confirm if all 3 files were found
            print(f"--- Indexer: Found {len(reader.input_files)} files and loaded {len(docs)} text chunks ---")
            
            if not docs:
                st.error("No PDF files found in the './data' folder.")
                return None

            # Create the index
            index = VectorStoreIndex.from_documents(docs)
            return index
            
        except Exception as e:
            st.error(f"Error loading files: {e}")
            return None

# 2. Fetch facts from the documents
def generate_response_index(chat_engine, user_prompt):
    try:
        response = chat_engine.chat(user_prompt)
        index_fact = response.response
        
        negative_keywords = ["i'm sorry", "not found", "don't have", "no documentation"]
        if any(word in index_fact.lower() for word in negative_keywords):
            return "No specific documentation found."
            
        return index_fact
    except Exception as e:
        return f"Index query error: {e}"

# 3. Extract keywords
def extract_keywords(chat_engine, text):
    query = f"Identify the 10 most important technical keywords in this text: {text}"
    response = chat_engine.chat(query)
    return response.response