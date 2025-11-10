import docker
import time
import sys

def test_scraper(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        time.sleep(5)  # Give container some time to print output
        logs = container.logs().decode("utf-8", errors="ignore")

        print("=== Container Logs ===")
        print(logs)

        # Basic checks
        if "Scraping" in logs or "<h1>" in logs or "<h2>" in logs:
            print("✅ Web scraper output looks valid.")
            return True
        else:
            print("❌ Expected scraper output not found.")
            return False

    except Exception as e:
        print(f"Error testing container: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_script_webscraper.py <container_name>")
        sys.exit(1)

    container_name = sys.argv[1]
    success = test_scraper(container_name)
    sys.exit(0 if success else 1)
