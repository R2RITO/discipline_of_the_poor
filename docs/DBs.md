# Database selection

To have multiple databases, each should be described in the DATABASES section
of the settings.py file, and created before running the project

### Middleware

In order to determine which database should be used, a middleware can be hooked
in the request process to save in a global variable (global per process using
a thread bound variable) the database name that should be used. To determine
this name, the middleware should a criteria such as location, user data or
similar.

To activate it, set the middleware:

    MIDDLEWARE = [
        . . .
        'budget.middlewares.db_middleware.RoutingMiddleware',
        . . .
    ]

### Router

When the database is about to be used, a router is called to determine the
database. Therefore, a custom router that checks the previously defined
global variable can be used to retrieve the database name to be used to either
read or write. To activate it:


    DATABASE_ROUTERS = [
        'budget.middlewares.db_middleware.CustomDatabaseRouter'
    ]


### Notes

This method of routing collides with the reversion database for unauthenticated
requests for a practical example, and as such is not active by default. To use
it, the middleware should be modified to define the database to be used
according to some other criteria of the request.
