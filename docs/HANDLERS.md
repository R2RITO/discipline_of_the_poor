# Dynamic handlers

To allow for flexibility in the projects behaviour on business logic, a way
is presented to give the administrator configuration access without having to
alter the source code.

This method is presented in the form of "handlers", a handler being a module
that implements an interface in a convenient way. Following a sense similar
to dependency injection, a function call to the base interface module can
determine at run-time the configured handler to execute using a dynamic import.

In this way, a database configuration can be used to fetch the correct handler
to use according to the business rules

### Base module

The base module should define the interface function call, that should be
the same in all the modules implementing the interface. Then, the handler
should be retrieved using importlib as such:

    module = importlib.import_module('route.to.handler_folder.' + handler_name)
    handler = getattr(module, 'handler_function_name')

    result = handler(**params)

### Improvements

This project does not provide a use case with databases, but a more useful
approach is to configure the handler names in a table (such as 
budget_stats_handlers), and then assign a foreign key to the desired object
(such as DotpUser) that points to the configurable handler.
(such as DotpUser) that points to the configurable handler.
