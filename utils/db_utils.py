import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Store DB locally
collection = chroma_client.get_or_create_collection("user_responses")

def store_user_response(question, user_answer, is_correct, response_time):
    """Stores user responses in ChromaDB."""
    data = f"Question: {question}\nAnswer: {user_answer}\nCorrect: {is_correct}\nTime Taken: {response_time:.2f} sec"
    collection.add(
        ids=[str(hash(question + user_answer))],  # Unique hash-based ID
        documents=[data]
    )

def get_past_responses():
    """Retrieves stored user responses from ChromaDB."""
    results = collection.get()
    return results["documents"] if "documents" in results else []

