import chromadb
from sentence_transformers import SentenceTransformer

# Load ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="posts")

# Load multilingual embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_embedding(text):
    """Generate embedding for the given text."""
    return model.encode(text).tolist()

def add_post_to_chroma(title, content):
    """Adds a post to ChromaDB with embeddings."""
    embedding = get_embedding(content)
    collection.add(
        ids=[title],
        documents=[content],
        metadatas=[{"title": title}]
    )

def search_posts(query, top_k=3):
    """Performs semantic search using ChromaDB."""
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return [{"title": r["title"], "content": d} for r, d in zip(results["metadatas"][0], results["documents"][0])]
