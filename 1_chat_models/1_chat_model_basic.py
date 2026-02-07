# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/


# poetry lock
# poetry install --no-root
# poetry env info
# eval $(poetry env activate)
# poetry show python-dotenv
# poetry env list

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

import google.generativeai as genai


# Load environment variables from .env
load_dotenv()

import os
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
for name, value in os.environ.items():
    if name in ("GOOGLE_API_KEY", "OPENAI_API_KEY"):
        print(name, value)

# Create a ChatOpenAI model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")

print("Full result:")
print(result)
print("Content only:")
print(result.content)
