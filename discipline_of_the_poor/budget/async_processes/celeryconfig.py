# Accept-Content settings
accept_content = ['application/x-python-serialize',
                  'application/json']
result_accept_content = ['application/x-python-serialize',
                         'application/json']

# Routes settings
task_routes = {
    'budget.async_processes.tasks': {'queue': 'dotp'},
}

# Timezone settings
enable_utc = False
timezone = 'America/Santo_Domingo'

# Worker settings
worker_send_task_events = True
