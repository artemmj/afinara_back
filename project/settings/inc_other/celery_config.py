import os

from celery.schedules import crontab

from ..common import env

BROKER_URL = os.environ.get('BROKER_URL', 'redis://redis/14')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis/15')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env('TIME_ZONE', str, 'Europe/Moscow')
CELERYBEAT_SCHEDULE = {
    "clear_pdf_filrs_dir_task": {
        "task": "apps.file.tasks.clear_pdf_files_dir",
        "schedule": crontab(hour=1, minute=0),
    },
}
