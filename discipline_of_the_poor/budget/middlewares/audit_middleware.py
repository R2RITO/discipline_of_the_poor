"""
Middleware used to manage the audit structure that saves the changes made
to models
"""
from budget.models.mixins import AuditTrailUser
import reversion
from reversion.middleware import RevisionMiddleware
from functools import wraps
from reversion.revisions import (
    create_revision as create_revision_base, set_user, get_user)
from reversion.views import _RollBackRevisionView
from reversion.views import _request_creates_revision
from reversion.views import _set_user_from_request


def _add_meta(request):
    """
    Adding session key to revision meta via VersionMeta model
    """
    token = request.headers.get('Authorization', u'')

    if token:
        user_info = payload_from_header(token)
        user_id = user_info.get('user_id')
    else:
        user_id = ''

    params = dict(
        user_id=user_id
    )
    reversion.add_meta(AuditTrailUser, **params)


def create_revision(manage_manually=False, using=None, atomic=True,
                    request_creates_revision=None):
    """
    View decorator that wraps the request in a revision.
    The revision will have it's user set from the request automatically.

    This is a re-implementation of reversion.views.create_revision that
    adds a call to `_add_meta` method on top of this file
    """
    request_creates_revision = (
            request_creates_revision or _request_creates_revision)

    def decorator(func):
        @wraps(func)
        def do_revision_view(request, *args, **kwargs):
            if request_creates_revision(request):
                try:
                    with create_revision_base(
                            manage_manually=manage_manually,
                            using=using,
                            atomic=atomic):
                        response = func(request, *args, **kwargs)
                        # Check for an error response.
                        if response.status_code >= 400:
                            raise _RollBackRevisionView(response)
                        # Otherwise, we're good.
                        _set_user_from_request(request)
                        # Additional call
                        _add_meta(request)
                        return response
                except _RollBackRevisionView as ex:
                    return ex.response
            return func(request, *args, **kwargs)
        return do_revision_view
    return decorator


class CustomAuditMiddleware(RevisionMiddleware):
    """
    Custom middleware, inheriting from RevisionMiddleware and using
    `create_revision` decorator re-implementation
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Support Django 1.10 middleware.
        if get_response is not None:
            self.get_response = create_revision(
                manage_manually=self.manage_manually,
                using=self.using,
                atomic=self.atomic,
                request_creates_revision=self.request_creates_revision
            )(get_response)
