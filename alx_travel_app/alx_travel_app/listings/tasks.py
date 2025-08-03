# listings/tasks.py

from celery import shared_task

@shared_task
def sample_task():
    print("This is a test task from Celery")
    return "Task complete"
