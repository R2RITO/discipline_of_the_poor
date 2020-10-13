"""
Module used to create the tasks needed to execute switch processes
"""
from budget.async_processes.celery_worker import celery_app
from budget.business.budget_periodic_movement.periodic_movement import (
    charge_periodic_movement)
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import CrontabSchedule
import json


def register_periodic_movement(periodic_movement):
    """
    Function used to register a movement charge task on the scheduler
    :param PeriodicMovement periodic_movement: instance to register
    :return:
    """
    period_type = periodic_movement.type
    period_time = periodic_movement.time

    if period_type == 'daily':
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=period_time.minute,
            hour=period_time.hour,
        )

    elif period_type == 'weekly':
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=period_time.minute,
            hour=period_time.hour,
            day_of_week=periodic_movement.day_of_week,
        )

    elif period_type == 'monthly':
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=period_time.minute,
            hour=period_time.hour,
            day_of_month=periodic_movement.day_of_month,
        )

    else:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=period_time.minute,
            hour=period_time.hour,
        )

    PeriodicTask.objects.create(
        crontab=schedule,
        name='Periodic movement ' + str(periodic_movement.id),
        task='budget.async_processes.tasks.charge_movement',
        kwargs=json.dumps({
            'movement_id': periodic_movement.id,
        }),
    )


@celery_app.task
def charge_movement(movement_id):
    return charge_periodic_movement(movement_id=movement_id)
