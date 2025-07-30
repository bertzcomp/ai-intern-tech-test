import os
import json
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv

DB_DIR = "chroma_db"
SUMMARIZE_FILE = "summarize_update.md"
TOP_K = 10

def generate_summary(year: str = "2024"):
    """
    This function loads relevant documents related to the Sales Management Hub (SMH)
    from a Chroma vector store, summarizes them using a Google Generative AI model,
    and saves the result to a Markdown file.

    Args:
        year (str): The year to generate the summary for. Defaults to "2024".
    """
    
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("API KEY not found!")
        return
    
    # Load the vector database from the ChromaDB directory
    if not os.path.exists(DB_DIR):
        print(f"Error: '{DB_DIR}' not found!, please create Vector DB first.")
        return
    
    print("Initializing model and load database\n\n")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embedding_model)

    # find the relevant documents 
    search_query = f"\nRingkasan Fitur pada SMH (Sales Management Hub) {year}"
    print(f"\n\nFinding {TOP_K} relevant documents for {search_query}")

    # Retrieve relevant documents using similarity search
    relevant_docs = vector_store.similarity_search(search_query, k=TOP_K)
    if not relevant_docs:
        print("There is no relevant documents")
        return
    print(f"\n\nFound {len(relevant_docs)} relevant documents")

    # Initialize the language model (LLM) for summarization
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)

    # Create a summarization chain using the LLM
    summary_chain = load_summarize_chain(llm, chain_type="stuff")

    print(f"\n\nSummarizing...\n\n")
    summary_result = summary_chain.invoke(relevant_docs)

    # Save the summary result to a Markdown file
    summarized = summary_result['output_text']
    with open(SUMMARIZE_FILE, "w", encoding='utf-8') as f:
        f.write(summarized)
    
    print(f"\n\nHasil rinkasan disimpan di '{SUMMARIZE_FILE}'")
    print(summarized)


if __name__ == "__main__":
    generate_summary(year="2024")