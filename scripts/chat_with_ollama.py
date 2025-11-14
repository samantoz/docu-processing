from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model="llama3", messages=[
    {
        "role": "user", 
        "content": "Hello, Who Are you!"
    }
])

print(response["message"]["content"])    