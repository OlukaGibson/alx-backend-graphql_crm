import requests
from datetime import datetime, timedelta
import json

query = """
query {
  orders(filter: { orderDateGte: "%s" }) {
    id
    customer {
      email
    }
  }
}
""" % (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

response = requests.post(
    "http://localhost:8000/graphql",
    json={"query": query},
    headers={"Content-Type": "application/json"}
)

orders = response.json().get("data", {}).get("orders", [])

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in orders:
        f.write(f"{timestamp} - Order ID: {order['id']}, Email: {order['customer']['email']}\n")

print("Order reminders processed!")
