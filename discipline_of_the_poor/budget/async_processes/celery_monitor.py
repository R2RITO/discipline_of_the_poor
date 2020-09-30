"""
Module used to provide monitor functions to workers
"""
from budget.async_processes.celery_worker import celery_app
from utils.email import send_failed_celery_task_alert


def failure_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])
        send_failed_celery_task_alert(task.uuid, task.name)

    with app.connection() as connection:
        recv = app.events.Receiver(
            connection,
            handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
            }
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    failure_monitor(celery_app)
