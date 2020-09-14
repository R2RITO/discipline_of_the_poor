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
        ]
        examples = {
            "username": "arturo",
            "password": "arturo",
            "first_name": "Arturo",
            "last_name": "Voltattorni",
            "email": "avoltattorni@ttt.com"
        }

        write_only_fields = ['password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = DotpUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
