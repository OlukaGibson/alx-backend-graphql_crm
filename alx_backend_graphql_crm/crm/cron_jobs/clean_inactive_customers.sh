#!/bin/bash

timestamp=$(date "+%Y-%m-%d %H:%M:%S")
deleted_count=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff).delete()
print(deleted)
")

echo \"$timestamp - Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
