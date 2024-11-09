import requests
import json
from ollama import Client

ollama_client = Client(host='http://localhost:11434')

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

    # payload = json.dumps({
    #     "model": model_name,
    #     "messages": sendMessages,
    #     "stream": False
    # })
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # response = requests.post('http://localhost:11434/api/chat',data=payload ,headers=headers)
    # if response.status_code == 200:
    #     return response.json()
    # else:
        # return {
        #     "err_code": response.status_code,
        #     "reason": response.reason,
        #     "request_body": response.request.body,
        #     "text": response.text
        # }
        