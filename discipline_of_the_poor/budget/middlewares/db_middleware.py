"""
Module used to create custom middleware
"""
from django.conf import settings
import threading
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from dotp_users.models.dotp_user import DotpUser


request_config = threading.local()


class RoutingMiddleware():
    """
    Middleware used to set the database to be used on the routing module based
    on the HTTP headers in the request
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        valid_dbs = settings.DATABASES

        # Fetch db according to customer's privilege
        try:
            user = JWTAuthentication().authenticate(request)

        except AuthenticationFailed as e:
            request_config.privilege_db = 'default'

        else:
            if not user:
                privilege = 'default'

            else:
                user = user[0]
                privilege = user.privilege

            request_config.privilege_db = privilege if valid_dbs.get(
                privilege, None) else 'default'

        # Continue chain
        response = self.get_response(request)

        if hasattr(request_config, 'privilege_db'):
            del request_config.privilege_db

        return response


class CustomDatabaseRouter():
    """
    Router used to check headers in order
    """
    def _get_db(self):
        """
        Method used to get the DB based on global variable
        :return:
        """
        if hasattr(request_config, 'privilege_db'):
            return request_config.privilege_db
        else:
            return 'default'

    def db_for_read(self, model, **hints):
        """
        Selects db to read.
        """
        return self._get_db()

    def db_for_write(self, model, **hints):
        """
        Selects db to write.
        """
        if model.__name__ == DotpUser.__name__:
            # Select db based on user privilege on creation
            return 'default'
        return self._get_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True
