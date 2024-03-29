import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("kale")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add the periodic task to the beat schedule
app.conf.beat_schedule = {
    'periodically-update-products': {
        'task': 'kale.main.tasks.update_products',
        'schedule': 4.0,  # Run every 1 minutes (in seconds)
    },
}
