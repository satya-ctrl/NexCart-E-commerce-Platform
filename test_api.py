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
            print("Successfully connected to Claude AI!")
            print(f"Response: {data['content'][0]['text']}")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(f"Body: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Extract API key from .env file manually since we don't want to rely on the server environment
    api_key = None
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if 'ANTHROPIC_API_KEY' in line and '=' in line:
                    api_key = line.split('=')[1].strip()
    
    if api_key:
        print(f"Testing API key: {api_key[:10]}...")
        test_claude(api_key)
    else:
        print("No ANTHROPIC_API_KEY found in .env")
