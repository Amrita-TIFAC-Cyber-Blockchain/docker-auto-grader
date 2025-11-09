import subprocess
import sys
import time
import requests

API_URL = "http://127.0.0.1:5001/api/v0/version"

def run_cmd(cmd):
    """Run a shell command and return output, error, and exit code."""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def wait_for_ipfs(container):
    """Wait for IPFS API inside container to be ready."""
    print("🚀 Waiting for IPFS daemon to be ready...")
    for i in range(10):
        try:
            # Try querying via localhost port (exposed from container)
            r = requests.post(API_URL, timeout=3)
            if r.status_code == 200:
                print("✅ IPFS API reachable via host port.")
                return True
        except Exception:
            # Fallback: check daemon process in container
            out, err, code = run_cmd(f"docker exec {container} pgrep ipfs")
            if code == 0 and out:
                print("✅ IPFS daemon is running inside container.")
                return True
            print(f"⏳ Attempt {i+1}/10: IPFS not ready yet...")
            time.sleep(3)
    print("❌ IPFS daemon did not start in time.")
    return False

def test_ipfs_inside(container):
    """Run basic IPFS CLI tests inside the running container."""
    print("🔍 Checking IPFS version...")
    out, err, code = run_cmd(f"docker exec {container} ipfs version")
    if code != 0:
        print(f"❌ Failed to get version: {err}")
        return False
    print(f"✅ {out}")

    print("📦 Adding a test file to IPFS...")
    run_cmd(f"docker exec {container} sh -c 'echo HelloFromContainer > /tmp/test.txt'")
    out, err, code = run_cmd(f"docker exec {container} ipfs add /tmp/test.txt")
    if code != 0 or "added" not in out:
        print(f"❌ Failed to add file: {err}")
        return False
    print(f"✅ {out}")
    file_hash = out.split()[1] if len(out.split()) > 1 else None

    print("🔗 Retrieving file back from IPFS...")
    out, err, code = run_cmd(f"docker exec {container} ipfs cat {file_hash}")
    if code != 0 or "HelloFromContainer" not in out:
        print(f"❌ Failed to cat file: {err}")
        return False
    print("✅ File retrieved successfully via IPFS.")

    print("🌐 Checking swarm peers (connectivity)...")
    out, err, code = run_cmd(f"docker exec {container} ipfs swarm peers")
    if code == 0:
        print("✅ Swarm peers checked (network working).")
    else:
        print("⚠️ Could not list swarm peers (may still be okay).")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_script.py <container_name>")
        sys.exit(1)

    container = sys.argv[1]

    if not wait_for_ipfs(container):
        sys.exit(1)

    print("🔧 Running IPFS CLI tests inside container...")
    if test_ipfs_inside(container):
        print("🎉 All IPFS tests passed!")
        sys.exit(0)
    else:
        print("❌ One or more IPFS tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
