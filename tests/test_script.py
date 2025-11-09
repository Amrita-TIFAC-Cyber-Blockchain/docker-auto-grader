import requests, sys, time

def wait_for_service(url, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

# Example test
if wait_for_service("http://localhost:8000"):
    r = requests.get("http://localhost:8000")
    if "Hello World" in r.text:
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL: Unexpected response")
        sys.exit(1)
else:
    print("FAIL: Service not reachable")
    sys.exit(1)
