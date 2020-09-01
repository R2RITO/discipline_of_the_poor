"""
Module used to handle the creation and updates of DotpUser objects
"""
from rest_framework import viewsets
from dotp_users.models.dotp_user import DotpUser
from dotp_users.serializers.dotp_user_serializer import DotpUserSerializer
#from budget.models.permission_signals import generate_permissions


class DotpUserViewSet(viewsets.ModelViewSet):
    queryset = DotpUser.objects.all()
    serializer_class = DotpUserSerializer

    permission_classes = []

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        user = DotpUser.objects.filter(id=result.data.get('id')).first()
        #permission_list = generate_permissions()
        #user.user_permissions.set(permission_list)

        return result
