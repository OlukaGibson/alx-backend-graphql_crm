INSTALLED_APPS = [
    # ...
    'graphene_django',
    'django_filters',
    'crm',
]

CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]