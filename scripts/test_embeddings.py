import random

def generate_mock_embedding(text):
    """Generates a mock embedding for given text."""
    return [random.random() for _ in range(128)]  # 128-dimensional vector

def store_embedding(embedding, id):
    """Simulates storing an embedding in a database."""
    # Replace this with actual database logic (e.g., OpenSearch)
    print(f"Embedding stored for ID {id}: {embedding[:5]}... (truncated)")

if __name__ == "__main__":
    # Simulate embedding generation for a document
    text = "This is a test document."
    embedding = generate_mock_embedding(text)
    store_embedding(embedding, id="test-id")
