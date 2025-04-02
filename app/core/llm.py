import os
from langfuse import Langfuse
from langfuse.openai import openai
from core import embeddings

# Load Langfuse credentials from environment variables
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

OPEN_ROUTER_AI_KEY = os.getenv('OPEN_ROUTER_AI_KEY')

if not OPEN_ROUTER_AI_KEY:
    raise ValueError("Missing API key: Set the OPEN_ROUTER_AI_KEY environment variable.")

if not LANGFUSE_PUBLIC_KEY:
    raise ValueError("Missing API key: Set the LANGFUSE_PUBLIC_KEY environment variable.")

client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= OPEN_ROUTER_AI_KEY
)

# Initialize Langfuse client
langfuse = Langfuse(public_key=LANGFUSE_PUBLIC_KEY, secret_key=LANGFUSE_SECRET_KEY)


def ask_ai(question):

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "system", "content": "You are a professional job interviewer."},
                  {"role": "user", "content": question}]
    )

    return completion.choices[0].message.content

def chat_with_ai(user_input, session, model_name, save_embeddings=True, use_rag=True):
    if "conversation" not in session:
        session["conversation"] = []

    user_prompt = "User Reply: " + user_input
    if use_rag :
        get_rag_results = embeddings.search_similar(user_input)
        if len(get_rag_results) > 5:
            user_prompt += "\n Relevant Examples:\n" + str(get_rag_results)

    # Append user input to history
    session["conversation"].append({"role": "user", "content": user_prompt})

    messages = session["conversation"]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    ai_response = response.choices[0].message.content

    if save_embeddings :
        # Store embeddings in Pinecone
        embeddings.store_embedding(user_input, "user")
        embeddings.store_embedding(ai_response, "assistant")

    # Append AI response to history
    session["conversation"].append({"role": "assistant", "content": ai_response})

    return ai_response

# Example:
#print(ask_ai("Tell me about yourself."))
