from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    try:
        res = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        status = res.json().get("data", {}).get("hello", "Unknown")
    except Exception as e:
        status = f"Error: {e}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive - GraphQL Status: {status}\n")

def update_low_stock():
    mutation = """
    mutation {
      updateLowStockProducts {
        success
        updatedProducts {
          name
          stock
        }
      }
    }
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            headers={"Content-Type": "application/json"}
        )
        updates = response.json()["data"]["updateLowStockProducts"]["updatedProducts"]
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for product in updates:
                f.write(f"{timestamp} - {product['name']} updated to stock {product['stock']}\n")
    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")
