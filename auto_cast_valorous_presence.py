#!/usr/bin/env python3
import sys
import requests

BASE = "https://habitica.com/api/v3"

# Habitica credentials
USER_ID = "42bf3777-022a-4b8d-abdf-176f7b8e7be9"
API_TOKEN = "b2d8430a-3c2d-45ba-9a40-af7372e00380"

HEADERS = {
    "x-api-user": USER_ID,
    "x-api-key": API_TOKEN,
    "x-client": f"{USER_ID}-habitica-script",
    "Content-Type": "application/json"
}

def _req(method, path):
    url = f"{BASE}{path}"
    r = requests.request(method, url, headers=HEADERS, timeout=20)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print(f"[ERROR] {method} {path} -> {r.status_code} {r.text}", flush=True)
        raise
    return r.json().get("data")

def get_party():
    return _req("GET", "/groups/party")

def get_content():
    return _req("GET", "/content")

def get_user():
    return _req("GET", "/user")

def cast_valorous_presence():
    return _req("POST", "/user/class/cast/valorousPresence")

def main() -> int:
    if not USER_ID or not API_TOKEN:
        print("[ERROR] HABITICA_USER_ID or HABITICA_API_TOKEN is missing.", flush=True)
        return 1

    # 1) Is there an active quest?
    try:
        party = get_party()
    except Exception:
        return 1

    quest = (party or {}).get("quest") or {}
    if not quest.get("active"):
        print("[INFO] No active quest; failing run (nothing to cast).", flush=True)
        return 1  # ❌ fail unless we actually cast

    quest_key = quest.get("key")
    if not quest_key:
        print("[INFO] No quest key found; failing run.", flush=True)
        return 1

    # 2) Boss vs collection?
    try:
        content = get_content()
    except Exception:
        return 1

    qdef = (content or {}).get("quests", {}).get(quest_key)
    if not qdef:
        print(f"[INFO] Quest '{quest_key}' not found in /content; failing run.", flush=True)
        return 1

    is_boss = bool(qdef.get("boss"))
    if not is_boss:
        print(f"[INFO] Quest '{quest_key}' is a collection quest; failing run (we only cast on boss).", flush=True)
        return 1  # ❌ fail unless we actually cast

    # 3) Cast — success only if this call goes through
    try:
        res = cast_valorous_presence()
        print(f"[OK] Cast Valorous Presence on boss quest '{quest_key}'. Response: {res}", flush=True)
        return 0  # ✅ success: we casted
    except Exception:
        # Already logged by _req
        return 1  # ❌ fail if cast didn't go through

if __name__ == "__main__":
    sys.exit(main())
