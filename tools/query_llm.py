import requests
import json
from ollama import Client

ollama_client = Client(host='http://localhost:11434') # http://192.168.2.231:11434

def query_llm(model_name='llama3:8b', system_prompt="", messages=[]):
    sendMessages = [
        {
            "role": "system",
            "content": system_prompt,
        },
    ]
    sendMessages.extend(messages)

    response = ollama_client.chat(model=model_name, messages=sendMessages, stream=False)
    return response
        