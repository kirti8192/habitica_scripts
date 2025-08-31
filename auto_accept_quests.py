import requests
import sys
import json

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

try:
    data = r.json()
except Exception:
    print("Quest Accept Response:", r.status_code, r.text)
    sys.exit(1)

print("Quest Accept Response:", r.status_code, json.dumps(data))

# Habitica sends {"success": True, "message": "You have accepted the quest."} when it worked
if r.ok and data.get("success") and "accepted" in (data.get("message") or "").lower():
    sys.exit(0)  # ✅ Success: quest accepted
else:
    sys.exit(1)  # ❌ Fail: no quest, already accepted, or error
