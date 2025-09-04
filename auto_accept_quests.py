import requests
import sys
import json
import os

user_id = os.environ["HABITICA_USER_ID"]
api_token = os.environ["HABITICA_API_TOKEN"]

url = "https://habitica.com/api/v3/groups/party/quests/accept"

headers = {
    "x-api-user": user_id,
    "x-api-key": api_token,
    "x-client": f"{user_id}-habitica-script",
    "Content-Type": "application/json"
}

r = requests.post(url, headers=headers)

try:
    data = r.json()
except Exception:
    print("Quest Accept Response:", r.status_code, r.text)
    sys.exit(1)

print("Quest Accept Response:", r.status_code, json.dumps(data))

# Habitica sends {"success": True, "message": "You have accepted the quest."} when it worked
if r.ok and data.get("success"):
    sys.exit(0)  # ✅ Success: quest accepted
else:
    sys.exit(1)  # ❌ Fail: no quest, already accepted, or error
