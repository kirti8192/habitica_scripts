import os
import requests

user_id = "42bf3777-022a-4b8d-abdf-176f7b8e7be9"
api_token = "b2d8430a-3c2d-45ba-9a40-af7372e00380"

url = "https://habitica.com/api/v3/groups/party/quests/accept"

headers = {
    "x-api-user": user_id,
    "x-api-key": api_token,
    "x-client": f"{user_id}-habitica-script",
    "Content-Type": "application/json"
}

r = requests.post(url, headers=headers)

print("Quest Accept Response:", r.status_code, r.json())
