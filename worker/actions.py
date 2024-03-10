from celery import Celery

from app.core.settings import settings
from worker.zero_crossings import calculate_zero_crossings

celery = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BACKEND_URL
)
celery.conf.broker_connection_retry_on_startup = True


@celery.task(name="on_ecg_create")
def on_ecg_create(ecg_id: int):
    return calculate_zero_crossings(ecg_id)
