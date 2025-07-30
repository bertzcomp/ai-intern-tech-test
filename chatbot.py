import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

#  Vector Database path
DB_DIRECTORY = "chroma_db"

def transform_query_with_time(query: str) -> str:
    '''Handle time-related keywords and convert them into more specific time range queries'''
    today = datetime.now()
    lower_query = query.lower()
    
    # Check for "hari ini"
    if "hari ini" in lower_query:
        date_str = today.strftime("%d %B %Y")
        return query.replace("hari ini", f"pada tanggal {date_str}")
        
    # Check for "minggu ini"
    elif "minggu ini" in lower_query:
        # Monday is considered the start of the week, and Sunday is the end.
        start_of_week = today + relativedelta(weekday=MO(-1))
        end_of_week = today + relativedelta(weekday=SU(1))
        date_range_str = f"antara {start_of_week.strftime('%d %B %Y')} dan {end_of_week.strftime('%d %B %Y')}"
        return query.replace("minggu ini", date_range_str)
        
    # Check for "bulan ini"
    elif "bulan ini" in lower_query:
        month_str = today.strftime("%B %Y")
        return query.replace("bulan ini", f"pada bulan {month_str}")
        
    # If no specific keyword is found, return the original query
    return query

def start_chatbot():
    '''# Set up the chatbot system using Google Generative AI'''

    load_dotenv()

    # Load the API key from environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found!")
        return
    # Load Vector Database
    if not os.path.exists(DB_DIRECTORY):
        print(f"Error: '{DB_DIRECTORY}' not found!, please create Vector DB first.")
        return

    print("Initializing model and load database...")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embedding_model)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)
    
    # Create a retriever to fetch a smaller number of documents for efficiency
    retriever = vector_store.as_retriever(
        search_kwargs={'k': 2}
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )

    print("\nSaya adalah AI yang akan membantu anda!")
    print('   Ketik "exit" atau "quit" untuk keluar.')

    while True:
        user_question = input("\nAnda: ")
        if user_question.lower() in ["exit", "quit"]:
            print("\nSampai jumpa!")
            break
        if user_question:
            # Transform the user's question into a more specific time-based query
            transformed_question = transform_query_with_time(user_question)
            print(f"Memproses pertanyaan sebagai: '{transformed_question}'...")
            
            hasil = qa_chain.invoke({"query": transformed_question})
            print(hasil["result"])
            print("\n---")
            print("Source:")
            for doc in hasil["source_documents"]:
                print(f"- {doc.metadata.get('feature_name', 'Dokumen tidak diketahui')}")
            print("---\n")

if __name__ == "__main__":
    start_chatbot()