"""
Module used to store mixin models such as timestamp mixins
or active mixins.
"""
from django.db import models
from reversion.models import Revision as RevisionModel


class BaseManager(models.Manager):
    """
    Base Manager for Base model, used to fetch only active objects
    """

    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class BaseMixin(models.Model):
    """
    Base class used to provide common attributes to each model
    """
    class Meta:
        abstract = True

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    hidden = models.BooleanField(default=False)

    objects = BaseManager()
    all_objects = models.Manager()

    # Override delete method.
    def delete(self, **kwargs):
        self._forced_delete = kwargs.pop('forced', False)
        if not self._forced_delete:
            self.hidden = True
            self.save()
        else:
            super().delete(**kwargs)


class AuditTrailUser(models.Model):
    user_id = models.CharField(max_length=9)
    full_name = models.CharField(max_length=100)
    revision = models.ForeignKey(RevisionModel,
                                 null=True,
                                 on_delete=models.SET_NULL)

    class Meta:
        managed = True
