# Audit trails

### Auditory

This project uses the django-reversion library to hook an audit trail model
that allows to track changes made to models. The library itself stores the
user_id of the current user that made the changes.

### Custom user

The project also includes a custom middleware useful to retrieve and store
additional info when the audit is saved. While not needed in this project, it
is included to show that more than the user_id can be saved in an audit.