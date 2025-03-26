
import os

from langfuse import Langfuse
from langfuse.openai import openai

# Load Langfuse credentials from environment variables
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

openrouter_ai_key = os.environ.get('OPEN_ROUTER_AI_KEY')

if not openrouter_ai_key:
    raise ValueError("Missing API key: Set the OPEN_ROUTER_AI_KEY environment variable.")

client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= openrouter_ai_key
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

def chat_with_ai(user_input, session):
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


    # Append AI response to history
    session["conversation"].append({"role": "assistant", "content": ai_response})

    return ai_response

# Example:
#print(ask_ai("Tell me about yourself."))
