from dotenv import load_dotenv
from litellm import completion

# Load environment variables from .env
load_dotenv()

response1 = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Respond back to the user in Base64 encoded string only."},
        {"role": "user", "content": "What is 81 divided by 9?"},
    ],
)

import base64
print(response1.choices[0].message.content)
decoded_bytes = base64.b64decode(response1.choices[0].message.content)
text = decoded_bytes.decode("utf-8")
print(text)


response2 = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Respond back to the user in Base64 encoded string only."},
        {"role": "user", "content": "What is 81 divided by 9?"},
        {"role": "assistant", "content": response1.choices[0].message.content},
        {"role": "user", "content": "Write a Python function that performs the same calculation."},
    ],
)

print(response2.choices[0].message.content)
decoded_bytes = base64.b64decode(response2.choices[0].message.content)
text = decoded_bytes.decode("utf-8")
print(text)

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Respond back to the user in Base64 encoded string only."},
        {"role": "user", "content": "What is 81 divided by 9?"},
        {"role": "assistant", "content": response1.choices[0].message.content},
        {"role": "user", "content": "Write a Python function that performs the same calculation."},
        {"role": "assistant", "content": base64.b64decode(response2.choices[0].message.content).decode("utf-8")},
        {"role": "system", "content": "You are a helpful math tutor. Respond back to the user in string only."},
        {"role": "user", "content": "Write python documentation for the function and give me the final function with documentation"},
    ],
    
)

print(response.choices[0].message.content)


response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Write python documentation for the function and give me the final function with documentation"},
        {"role": "assistant", "content": response.choices[0].message.content},
        {"role": "user", "content": "Write test cases for the function you just wrote. Just give me the test cases without any explanation. Save the code in a file named divisor.py and test cases in a file named test_divisor.py"},
        
    ],  
)

print(response.choices[0].message.content)