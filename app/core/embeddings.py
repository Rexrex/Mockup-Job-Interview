import os
import uuid
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "interview-conversations"

# Check if index exists, if not, create it
if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {
                "text": "text"  # Map the record field to be embedded
            }
        }
    )

index = pc.Index(index_name)  # Initialize the index

def store_embedding(text, role):
    record_id = str(uuid.uuid4())  # Generates a unique ID every time
    new_record = [{"_id": record_id, "text": text, "role":role}]
    index.upsert_records(index_name, new_record)


def search_similar(text):
    results = index.search(
        namespace=index_name,
        query={
            "inputs": {"text": text},
            "top_k": 3
        },
        fields=["text", "role"]
    )
    print("RAG Results\n" + str(results))

    # Extract text from search results
    retrieved_texts = [
        {"text": hit["fields"].get("text", "No text found"), "role": hit["fields"].get("role", "unknown")}
        for hit in results["result"]["hits"]
    ]

    print("Translated RAG Results\n", retrieved_texts)
    return results