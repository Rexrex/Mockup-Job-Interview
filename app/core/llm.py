
import os
import uuid
from pinecone import Pinecone, ServerlessSpec
from langfuse import Langfuse
from langfuse.openai import openai

# Load Langfuse credentials from environment variables
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

openrouter_ai_key = os.environ.get('OPEN_ROUTER_AI_KEY')

openai_api_key = os.environ.get('OPENAI_API_KEY')

if not openrouter_ai_key:
    raise ValueError("Missing API key: Set the OPEN_ROUTER_AI_KEY environment variable.")

client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= openrouter_ai_key
)

embeddings_client = openai.OpenAI(
  api_key= openai_api_key
)

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
global current_index
current_index = 0

# Initialize Langfuse client
langfuse = Langfuse(public_key=LANGFUSE_PUBLIC_KEY, secret_key=LANGFUSE_SECRET_KEY)

# Function to store embeddings
def store_embedding(text, role):
    global current_index
    new_record = [{"_id": "vec" + str(current_index), "text": text, "role":role}]
    index.upsert_records(index_name, new_record)
    current_index += 1


def search_similar(text):
    results = index.query(
        vector=None,  # ✅ Let Pinecone generate embeddings
        top_k=5,
        include_metadata=True
    )
    return results

def ask_ai(question):

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "system", "content": "You are a professional job interviewer."},
                  {"role": "user", "content": question}]
    )

    return completion.choices[0].message.content

def chat_with_ai(user_input, session, save_embeddings=True):
    if "conversation" not in session:
        session["conversation"] = []

    # Append user input to history
    session["conversation"].append({"role": "user", "content": user_input})

    messages = session["conversation"]

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages
    )

    ai_response = response.choices[0].message.content

    if(save_embeddings):
        # Store embeddings in Pinecone
        store_embedding(user_input, "user")
        store_embedding(ai_response, "assistant")

    # Append AI response to history
    session["conversation"].append({"role": "assistant", "content": ai_response})

    return ai_response

# Example:
#print(ask_ai("Tell me about yourself."))
