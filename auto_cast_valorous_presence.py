#!/usr/bin/env python3
import sys
import requests

BASE = "https://habitica.com/api/v3"

# Habitica credentials
user_id = "42bf3777-022a-4b8d-abdf-176f7b8e7be9"
api_token = "b2d8430a-3c2d-45ba-9a40-af7372e00380"

HEADERS = {
    "x-api-user": user_id,
    "x-api-key": api_token,
    "x-client": f"{user_id}-habitica-script",
    "Content-Type": "application/json"
}

def _req(method, path):
    url = f"{BASE}{path}"
    r = requests.request(method, url, headers=HEADERS, timeout=20)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print(f"[ERROR] {method} {path} -> {r.status_code} {r.text}", flush=True)
        raise
    return r.json()["data"]

def get_party():
    return _req("GET", "/groups/party")

def get_content():
    return _req("GET", "/content")

def get_user():
    return _req("GET", "/user")

def cast_valorous_presence():
    return _req("POST", "/user/class/cast/valorousPresence")

def main():
    if not USER_ID or not API_TOKEN:
        print("[ERROR] HABITICA_USER_ID or HABITICA_API_TOKEN is missing.", flush=True)
        sys.exit(1)

    # 1) Is there an active quest?
    party = get_party()
    quest = party.get("quest") or {}
    if not quest or not quest.get("active"):
        print("[INFO] No active quest; skipping cast.", flush=True)
        return

    quest_key = quest.get("key")
    if not quest_key:
        print("[INFO] No quest key found; skipping cast.", flush=True)
        return

    # 2) Look up quest definition to determine type (boss vs collection)
    content = get_content()
    quests = content.get("quests", {})
    qdef = quests.get(quest_key)
    if not qdef:
        print(f"[INFO] Quest '{quest_key}' not found in /content; skipping cast.", flush=True)
        return

    is_boss = bool(qdef.get("boss"))
    if not is_boss:
        print(f"[INFO] Quest '{quest_key}' is a collection quest; skipping cast to save MP.", flush=True)
        return

    # 3) Cast
    try:
        res = cast_valorous_presence()
        print(f"[OK] Cast Valorous Presence on boss quest '{quest_key}'. Response: {res}", flush=True)
    except Exception:
        # Already logged by _req
        # Don’t fail the whole workflow just because the cast didn’t go through
        pass

if __name__ == "__main__":
    main()