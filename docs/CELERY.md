# Celery scheduled tasks

The project uses celery and django_celery_beat to manage all periodic tasks
such as charging the budget on periodic movements.

To achieve this, a package called async_processes is used, in which the
required files are defined. For this project, RabbitMQ is used as a broker
for the messages, and a very minimal configuration is used for the tasks.

### Worker

The worker is in charge of running the tasks in the work queue, so it should
have the same code of the task's sender, and should run in a separate process

### Tasks

The tasks module defines the task to execute which calls the function used
to charge the budget, and provides a function to register a scheduled task
in the django celery beat scheduler in order to dynamically register new
periodic tasks. The scheduler has to be run in a separate process than the
worker and the main project.

### Monitoring

The monitoring module provides e-mail notifications when a task fails, and
should be run on a separate process as well.