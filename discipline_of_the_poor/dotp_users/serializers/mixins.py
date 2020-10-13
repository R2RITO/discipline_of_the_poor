"""
Module used to store serializer mixins useful for custom methods
"""
from rest_framework import serializers


class OwnerModelSerializerMixin(serializers.ModelSerializer):
    """
    Class to be used as a parent by serializers of models who inherit
    from OwnershipMixin themselves. This serializer passes the owner as
    a field on the validated_data dict. If no user is found, an exception
    will be thrown
    """
    class Meta:
        fields = ['owner']
        read_only_fields = ['owner']
        abstract = True

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(OwnerModelSerializerMixin, self).create(validated_data)
