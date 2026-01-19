"""
Simple Prospeo API test - minimal request to check connection
"""
import requests
import config

# Test basic connection
headers = {
    "X-KEY": config.PROSPEO_API_KEY,
    "Content-Type": "application/json"
}

# Try minimal request first
print("Testing Prospeo API connection...")
print(f"API Key starts with: {config.PROSPEO_API_KEY[:15]}...")
print(f"Endpoint: {config.PROSPEO_SEARCH_PERSON_ENDPOINT}")
print()

# Test 1: Minimal payload
print("Test 1: Minimal payload (no filters)")
payload1 = {
    "page": 1,
    "limit": 10
}

try:
    response = requests.post(
        config.PROSPEO_SEARCH_PERSON_ENDPOINT,
        json=payload1,
        headers=headers,
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Success! Received {len(data.get('data', []))} persons")
        print(f"Response keys: {list(data.keys())}")
    else:
        print(f"[ERROR] Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"[ERROR] Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 2: With simple filters
print("Test 2: With simple keyword filter")
payload2 = {
    "page": 1,
    "limit": 10,
    "filters": {
        "keywords": "SaaS"
    }
}

try:
    response = requests.post(
        config.PROSPEO_SEARCH_PERSON_ENDPOINT,
        json=payload2,
        headers=headers,
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Success! Received {len(data.get('data', []))} persons")
    else:
        print(f"[ERROR] Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"[ERROR] Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 3: Check if we need different header format
print("Test 3: Alternative header format (Authorization)")
headers2 = {
    "Authorization": f"Bearer {config.PROSPEO_API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        config.PROSPEO_SEARCH_PERSON_ENDPOINT,
        json=payload1,
        headers=headers2,
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"[OK] Success with Authorization header!")
    else:
        print(f"[ERROR] Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"[ERROR] Exception: {e}")
