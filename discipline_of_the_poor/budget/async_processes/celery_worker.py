"""
Module used to define the celery "app" to be called to run the server and
register the tasks
"""
import os
from celery import Celery
from django.conf import settings
from budget.async_processes import celeryconfig


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discipline_of_the_poor.settings')

celery_app = Celery('dotp',
                    broker=settings.CELERY_BROKER,
                    include=['budget.async_processes.tasks'])

celery_app.config_from_object('budget.async_processes.celeryconfig')


if __name__ == '__main__':
    celery_app.start()
