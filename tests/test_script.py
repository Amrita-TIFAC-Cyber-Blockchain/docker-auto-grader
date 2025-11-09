import subprocess
import time
import sys
import requests
import os

API_URL = "http://127.0.0.1:5001/api/v0/version"

def run_command(cmd, timeout=10):
    """Run a shell command safely and capture its output."""
    try:
        result = subprocess.run(
            cmd, shell=True, text=True, capture_output=True, timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1

def wait_for_ipfs_daemon(max_retries=10):
    """Wait for IPFS API to become available."""
    print("🚀 Waiting for IPFS daemon to be ready...")
    for i in range(max_retries):
        try:
            response = requests.post(API_URL, timeout=3)
            if response.status_code == 200:
                print("✅ IPFS API is reachable.")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1}/{max_retries}: IPFS not ready yet ({e})")
        time.sleep(3)
    print("❌ IPFS daemon did not start in time.")
    return False

def check_ipfs_cli():
    """Ensure IPFS CLI is installed."""
    out, err, code = run_command("ipfs --version")
    if code != 0:
        print("❌ IPFS CLI not found on runner:", err)
        return False
    print("✅ IPFS CLI available:", out)
    return True

def test_ipfs_commands():
    """Run a series of functional IPFS CLI tests."""
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
        print("❌ Failed to add file:", err)
        return False
    print("✅ File added:", out)

    # Extract file hash safely
    parts = out.split()
    file_hash = next((p for p in parts if len(p) >= 46 and p.startswith("Qm")), None)
    if not file_hash:
        print("❌ Could not parse file hash from output.")
        return False

    print(f"🔗 Verifying file retrieval via hash: {file_hash}")
    out, err, code = run_command(f"ipfs cat {file_hash}")
    if code != 0 or "Hello" not in out:
        print("❌ Failed to read file:", err)
        return False
    print("✅ File retrieved successfully.")

    print("🔎 Testing IPFS network peers (optional)...")
    out, err, code = run_command("ipfs swarm peers")
    if code == 0:
        print(f"✅ Connected peers: {len(out.splitlines())}")
    else:
        print("⚠️ No peers connected (this may be fine in isolated test mode).")

    return True

def main():
    print("=============================")
    print("Running IPFS Auto-Grader Tests")
    print("=============================")

    if not check_ipfs_cli():
        sys.exit(1)
    if not wait_for_ipfs_daemon():
        sys.exit(1)

    print("🔧 Running IPFS functional tests...")
    if test_ipfs_commands():
        print("🎉 All IPFS tests passed!")
        sys.exit(0)
    else:
        print("❌ One or more IPFS tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
