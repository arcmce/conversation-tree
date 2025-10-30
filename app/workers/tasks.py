from app.workers.celery_app import celery_app

@celery_app.task(name="app.workers.tasks.add")
def add(x, y):
    return x + y