import json
import urllib.request
import urllib.error
import os


def test_claude(api_key):
    """Test Anthropic Claude API"""
    payload = json.dumps({
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hello"}]
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print("[OK] Claude AI: Connected successfully!")
            print(f"     Claude Response: {data['content'][0]['text'].strip()}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[FAIL] Claude AI HTTP Error: {e.code} - {e.reason}")
        print(f"       Response Body: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"[ERROR] Claude AI Connection Error: {str(e)}")
        return False


def test_gemini(api_key):
    """Test Google Gemini API"""
    payload = json.dumps({
        "contents": [{"parts": [{"text": "Hello"}]}]
    }).encode('utf-8')

    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print("[OK] Gemini AI: Connected successfully!")
            print(f"     Gemini Response: {data['candidates'][0]['content']['parts'][0]['text'].strip()}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[FAIL] Gemini AI HTTP Error: {e.code} - {e.reason}")
        print(f"       Response Body: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"[ERROR] Gemini AI Connection Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("           NexCart AI API Connectivity Tester")
    print("=" * 60)
    
    claude_api_key = None
    gemini_api_key = None
    
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip()
                    if k == 'ANTHROPIC_API_KEY':
                        claude_api_key = v
                    elif k == 'GEMINI_API_KEY':
                        gemini_api_key = v
                        
    # Also check os.environ
    claude_api_key = claude_api_key or os.environ.get('ANTHROPIC_API_KEY')
    gemini_api_key = gemini_api_key or os.environ.get('GEMINI_API_KEY')
    
    print("\n[1] Testing Claude AI Connectivity:")
    if claude_api_key:
        print(f"    Key loaded: {claude_api_key[:10]}...")
        test_claude(claude_api_key)
    else:
        print("    No ANTHROPIC_API_KEY configured.")

    print("\n[2] Testing Gemini AI Connectivity:")
    if gemini_api_key:
        print(f"    Key loaded: {gemini_api_key[:10]}...")
        test_gemini(gemini_api_key)
    else:
        print("    No GEMINI_API_KEY configured.")
        
    print("\n" + "=" * 60)
