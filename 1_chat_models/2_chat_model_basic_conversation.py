from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# SystemMessage:
#   Message for priming AI behavior, usually passed in as the first of a sequenc of input messages.
# HumanMessagse:
#   Message from a human to the AI model.
messages = [
    SystemMessage(content="Solve the following math problems"),
    HumanMessage(content="What is 81 divided by 9?"),
]

# Invoke the model with messages
result = model.invoke(messages)
print(f"Answer from AI: Total Tokens {result.response_metadata['token_usage']['total_tokens']}, Content {result.content}")


# AIMessage:
#   Message from an AI.
messages = [
    SystemMessage(content="Solve the following math problems and respond back in the same manner as i showed"),
    HumanMessage(content="What is 81 divided by 9?"),
    AIMessage(content="==> 81/9 = 9"),
    HumanMessage(content="What is 27 divided by 9?"),
    AIMessage(content="==> 27/9 = 3"),
    HumanMessage(content="What is 51 divided by 17?"),
    AIMessage(content="==> 51/17 = 3"),
    HumanMessage(content="What is 10 divided by 5?"),
]

# Invoke the model with messages
result = model.invoke(messages)
print(f"Answer from AI: Total Tokens {result.response_metadata['token_usage']['total_tokens']}, Content {result.content}")

