import requests
import json
from openaikey import OPENAI_KEY

# result = requests.get("https://wheretheiss.at/w/ajax/realtime")
# print(result.text)


openai_endpoint = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {OPENAI_KEY}"
}

data = {
    "model":"gpt-4o",
    "messages":[
        {
            "role":"user",
            "content":"Respond with some positive emojis"
        }
    ]
}

response = requests.post(openai_endpoint, headers=headers, json=data)

print(response.text)