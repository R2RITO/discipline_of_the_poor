"""
Module used to store the BudgetShare serializer class, used to
serialize a request to update a budget's permissions, in order to allow
sharing
"""
from budget.models.budget import Budget
from django.contrib import auth
from rest_framework import serializers
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from guardian.shortcuts import get_perms
from django.utils.translation import gettext as _


PERM_CHOICES = [
    ('change', _('Change')),
    ('view', _('View')),
]

PERM_ACTION_CHOICES = [
    ('add', _('Add permissions')),
    ('remove', _('Remove permissions')),
]


class BudgetShareSerializer(serializers.Serializer):

    username = serializers.CharField()
    shared_permissions = serializers.MultipleChoiceField(
        choices=PERM_CHOICES,
        required=True,
    )
    action = serializers.ChoiceField(
        choices=PERM_ACTION_CHOICES,
        write_only=True,
        required=True,
    )

    class Meta:
        model = Budget
        fields = ['username', 'shared_permissions', 'action']

    def update(self, instance, validated_data):
        """
        Method used to update permissions on an object
        :param instance:
        :param validated_data:
        :return:
        """
        try:
            user = auth.get_user_model().objects.get(
                username=validated_data.get('username'))
        except auth.get_user_model().DoesNotExist as e:
            raise serializers.ValidationError(_('Invalid username'))

        action = validated_data.get('action')

        # Validate that the owner does not change its own permissions
        if self.context.get('request').user == user:
            raise serializers.ValidationError(
                _('Cannot change owner permissions'))

        # Update for this user
        for perm in validated_data.get('shared_permissions'):
            if action == 'add':
                assign_perm(perm + '_' + self.Meta.model.__name__.lower(),
                            user,
                            instance)
            else:
                remove_perm(perm + '_' + self.Meta.model.__name__.lower(),
                            user,
                            instance)

        updated_perms = {p.split('_')[0] for p in get_perms(user, instance)}
        payload = {
            'username': user.get_username(),
            'shared_permissions': updated_perms
        }

        return payload
