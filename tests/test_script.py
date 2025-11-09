import subprocess
import time
import sys
import requests

API_URL = "http://127.0.0.1:5001/api/v0/version"

def run_command(cmd):
    """Run a shell command and capture output."""
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "TimeoutExpired", 1


def wait_for_ipfs_daemon():
    """Wait for IPFS API to come up."""
    print("🚀 Waiting for IPFS daemon to be ready...")
    for i in range(10):
        try:
            response = requests.post(API_URL, timeout=3)
            if response.status_code == 200:
                print("✅ IPFS API is reachable.")
                return True
        except Exception as e:
            print(f"Attempt {i+1}: IPFS not ready yet ({e})")
            time.sleep(3)
    print("❌ IPFS daemon did not start in time.")
    return False


def test_ipfs_commands():
    """Run a few basic IPFS CLI commands."""
    print("🔍 Checking IPFS version...")
    out, err, code = run_command("ipfs version")
    if code != 0:
        print("❌ Failed to get IPFS version:", err)
        return False
    print("✅", out)

    print("📦 Adding a test file to IPFS...")
    with open("sample.txt", "w") as f:
        f.write("Hello from GitHub Actions IPFS Test!")
    out, err, code = run_command("ipfs add sample.txt")
    if code != 0:
        print("❌ Failed to add file to IPFS:", err)
        return False
    print("✅ File added:", out)
    file_hash = out.split()[-2] if len(out.split()) >= 2 else None

    print("🔗 Trying to cat the file from IPFS...")
    out, err, code = run_command(f"ipfs cat {file_hash}")
    if code != 0 or "Hello" not in out:
        print("❌ Unable to read back file from IPFS:", err)
        return False
    print("✅ File retrieved successfully.")

    return True


def main():
    if not wait_for_ipfs_daemon():
        sys.exit(1)

    print("🔧 Running IPFS CLI tests...")
    if test_ipfs_commands():
        print("🎉 All IPFS tests passed!")
        sys.exit(0)
    else:
        print("❌ IPFS tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
