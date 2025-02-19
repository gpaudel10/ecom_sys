# celeryconfig.py

from app.core.config import settings

broker_url = settings.REDIS_URL
result_backend = settings.REDIS_URL
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
task_routes = {
    'app.workers.email_worker.*': {'queue': 'email'}
}