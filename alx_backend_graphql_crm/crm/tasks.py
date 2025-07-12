from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    query = """
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """
    response = requests.post("http://localhost:8000/graphql", json={"query": query})
    data = response.json().get("data", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} - Report: {data.get('totalCustomers')} customers, {data.get('totalOrders')} orders, {data.get('totalRevenue')} revenue\n"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log)
