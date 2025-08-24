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

# Load environment variables from .env
load_dotenv()

import os
for name, value in os.environ.items():
    if name in ("OPENAI_API_KEY"):
        print(name, value)

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")

print("Full result:")
print(result)
print("Content only:")
print(result.content)
