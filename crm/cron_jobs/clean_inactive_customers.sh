#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Navigate to project root
cd "$PROJECT_DIR" || exit 1

# Activate virtual environment if needed (optional)
# source venv/bin/activate

timestamp=$(date "+%Y-%m-%d %H:%M:%S")

deleted_count=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff).delete()
print(deleted)
")
alx-backend-graphql_crm/crm/cron_jobs/clean_inactive_customers.sh
# Check if deletion succeeded
if [ $? -eq 0 ]; then
    echo "$timestamp - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$timestamp - Cleanup script failed" >> /tmp/customer_cleanup_log.txt
fi
