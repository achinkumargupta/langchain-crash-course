# LiteLLM Example with Google Gemini
# Documentation: https://docs.litellm.ai/

from dotenv import load_dotenv
from litellm import completion
import os

# Load environment variables from .env
load_dotenv()

# ---- List Available Google Models ----
print("=== Available Google Gemini Models ===")
google_api_key = os.environ.get("GOOGLE_API_KEY")

print("\n=== Simple Completion Example ===")

# ---- Simple Completion with litelLM ----
# LiteLLM model format for Google: "google/gemini-1.5-flash"

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "What is 81 divided by 9?"},
    ],
)

print("Response:")
print(response)
print("\nContent only:")

print(response.choices[0].message.content)

print("\n=== Streaming Example ===")

# ---- Streaming Response ----
response_stream = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "List 3 fun facts about Python programming."},
    ],
    api_key=google_api_key,
    stream=True,
)

print("Streaming response:")
for chunk in response_stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print("\n")
