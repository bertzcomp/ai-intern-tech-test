import json
import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

#  Config file path
JSON_FILE_PATH = "dataset/simplidots.json"
DB_DIR = "chroma_db"

def build_vector_database():
    """
    Loads text data from a JSON file,  converts it into LangChain documents, 
    mbeds them using Google Generative AI, and stores the resulting vectors 
    in a ChromaDB directory.
    """
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found!")
        return

    # Load data from json file
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            all_chunks = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{JSON_FILE_PATH}' file not found!")
        return

    # tranform data type into Langchain Object Document
    documents = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in all_chunks
    ]
    print(f"\nBerhasil memuat {len(documents)} dokumen dari file JSON.")

    # Initialization model embedding
    print("\nInisiasi model embedding...")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create Vector Database and save it
    print(f"Membuat dan menyimpan vector store ke direktori '{DB_DIR}'...")
    if os.path.exists(DB_DIR):
        print(f"Direktori '{DB_DIR}' sudah ada. Akan menimpa data lama.")
    
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=DB_DIR
    )

    print(f"\nProses indexing selesai! Database vektor telah disimpan di '{DB_DIR}'.")

if __name__ == "__main__":
    build_vector_database()
