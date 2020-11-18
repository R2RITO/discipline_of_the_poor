"""
Module used to store the TherappyUser serializer class, used to
serialize a user
"""
from dotp_users.models.dotp_user import DotpUser
from rest_framework import serializers


class DotpUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DotpUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'privilege',
            'notify_low_budget_amount',
        ]
        examples = {
            "username": "arturo",
            "password": "arturo",
            "first_name": "Arturo",
            "last_name": "Voltattorni",
            "email": "avoltattorni@ttt.com",
            "privilege": "premium",
            "notify_low_budget_amount": True,
        }

        write_only_fields = ['password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }

        if validated_data.get('privilege'):
            user_data['privilege'] = validated_data.get('privilege')

        user = DotpUser.objects.create(**user_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
