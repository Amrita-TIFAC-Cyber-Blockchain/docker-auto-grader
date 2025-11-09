import requests
import time

URL = "http://localhost:8080"
MAX_RETRIES = 5

for attempt in range(MAX_RETRIES):
    try:
        response = requests.get(URL, timeout=5)
        print(f"Attempt {attempt+1}: Status {response.status_code}")
        if response.status_code == 200:
            print("✅ Web server is responding correctly.")
            exit(0)
    except Exception as e:
        print(f"Attempt {attempt+1}: Connection failed ({e})")
        time.sleep(3)

print("❌ Server not reachable on port 8080 after retries.")
exit(1)
