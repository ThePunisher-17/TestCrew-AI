# components/vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer
# --- NEW IMPORT ---
from .analytics import get_questions_by_ids

# Initialize a persistent ChromaDB client
client = chromadb.PersistentClient(path="db/chroma_db")
# Load a sentence transformer model for creating embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Get or create a collection for our questions
question_collection = client.get_or_create_collection(name="gate_questions")

def add_question_to_rag(question_id: int, question_text: str):
    """Adds a new question's embedding to the vector store."""
    embedding = embedding_model.encode(question_text).tolist()
    question_collection.add(
        embeddings=[embedding],
        documents=[question_text],
        ids=[str(question_id)]
    )

def find_similar_question(question_text: str, threshold=0.98) -> bool:
    """Checks if a highly similar question already exists in the RAG store."""
    if question_collection.count() == 0:
        return False

    query_embedding = embedding_model.encode(question_text).tolist()
    results = question_collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    if results and results['distances'] and results['distances'][0]:
        similarity_score = 1 - results['distances'][0][0]
        if similarity_score > threshold:
            print(f"⚠️ Found a similar question with score: {similarity_score:.2f} (Threshold: {threshold}). Regenerating...")
            return True
            
    return False

# --- UPDATED FUNCTION ---
def search_questions(query: str, n_results=5) -> list[dict]:
    """Searches RAG, gets IDs, and returns full question data from SQLite."""
    if question_collection.count() == 0:
        return []

    query_embedding = embedding_model.encode(query).tolist()
    results = question_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    if not results or not results.get('ids')[0]:
        return []
        
    question_ids = results['ids'][0]
    full_questions = get_questions_by_ids(question_ids)
    
    return full_questions