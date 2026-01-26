"""
Diagnose OpenRouter connectivity and auth.
Run from project root:  python diagnose_openrouter.py

Use this when every wholesale_partner_response in Supabase is "Error: 401" or similar.
"""
import os
import sys

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    print("=== OpenRouter diagnostic ===\n")

    key = os.getenv("OPENROUTER_API_KEY")
    base = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b")

    # 1. Env check
    if not key or not str(key).strip():
        print("OPENROUTER_API_KEY: NOT SET or empty")
        print()
        print("NEXT STEPS:")
        print("  1. Get a key from https://openrouter.ai (Keys or API Keys).")
        print("  2. In this project folder, open or create .env")
        print("  3. Add this line (use your real key, no quotes):")
        print("     OPENROUTER_API_KEY=sk-or-v1-your-key-here")
        print("  4. Save .env and run this script again from the project folder.")
        print()
        print("  If the app runs on Railway, also add OPENROUTER_API_KEY in Railway Variables and redeploy.")
        return 1
    key_preview = key[:12] + "..." + key[-4:] if len(key) > 20 else "***"
    print(f"OPENROUTER_API_KEY: set ({len(key)} chars, {key_preview})")
    print(f"OPENROUTER_BASE_URL: {base}")
    print(f"OPENROUTER_MODEL: {model}")
    print()

    # 2. One minimal request
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=base)
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with one word: OK"}],
            max_tokens=5,
        )
        text = (r.choices[0].message.content or "").strip()
        print("OpenRouter request: SUCCESS")
        print(f"  Response: {text}")
        print()
        print("  If Supabase still shows 401, the app is not using this key. Set OPENROUTER_API_KEY")
        print("  in the place the app runs (e.g. Railway Variables) and redeploy. See OPENROUTER_401_TROUBLESHOOTING.md")
        return 0
    except Exception as e:
        print("OpenRouter request: FAILED")
        print(f"  Exception type: {type(e).__name__}")
        print(f"  Exception message: {e}")

        # Try to surface status code from common error attributes
        if hasattr(e, "status_code"):
            print(f"  status_code: {e.status_code}")
        if hasattr(e, "response") and e.response is not None:
            if hasattr(e.response, "status_code"):
                print(f"  response.status_code: {e.response.status_code}")
            if hasattr(e.response, "text"):
                body = (e.response.text or "")[:500]
                print(f"  response body (truncated): {body}")

        print()
        print("NEXT STEPS:")
        print("  1. Open https://openrouter.ai and create or copy a valid API key (starts with sk-or-v1-).")
        print("  2. In this project folder, edit .env and set:")
        print("     OPENROUTER_API_KEY=your-key  (no quotes, no extra spaces)")
        print("  3. Save and run this script again. If it still fails, create a NEW key at openrouter.ai.")
        print("  4. If your app runs on Railway: add OPENROUTER_API_KEY in Railway Variables, then redeploy.")
        print()
        print("  Full guide: OPENROUTER_401_TROUBLESHOOTING.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
