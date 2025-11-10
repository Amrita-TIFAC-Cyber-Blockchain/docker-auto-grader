import docker
import sys
import time

def test_dbconnector(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        time.sleep(5)  # Wait for logs to appear
        logs = container.logs().decode("utf-8", errors="ignore")

        print("=== Container Logs ===")
        print(logs)

        # Expected patterns
        if any(keyword in logs for keyword in ["Connecting", "connection", "Connected", "Database"]):
            print("✅ Database connector output looks valid.")
            return True
        else:
            print("❌ Expected DB connection output not found.")
            return False

    except Exception as e:
        print(f"Error testing container: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_script_dbconnector.py <container_name>")
        sys.exit(1)

    container_name = sys.argv[1]
    success = test_dbconnector(container_name)
    sys.exit(0 if success else 1)
