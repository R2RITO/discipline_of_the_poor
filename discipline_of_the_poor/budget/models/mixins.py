"""
Module used to store mixin models such as timestamp mixins
or active mixins.
"""
from django.db import models


class BaseManager(models.Manager):
    """
    Base Manager for Base model, used to fetch only active objects
    """

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class BaseMixin(models.Model):#OwnershipMixin):
    """
    Base class used to provide common attributes to each model
    """
    class Meta:
        abstract = True

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    objects = BaseManager()
    all_objects = models.Manager()

    # Override delete method.
    def delete(self, **kwargs):
        self._forced_delete = kwargs.pop('forced', False)
        if not self._forced_delete:
            self.active = False
            self.save()
        else:
            super().delete(**kwargs)
