"""
View used to let the user activate or deactivate low budget available
amount notifications
"""
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from budget.serializers.notify_low_budget_amount_serializer import (
    NotifyLowBudgetAmountSerializer)


class NotifyLowBudgetAmountView(views.APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @swagger_auto_schema(
        request_body=NotifyLowBudgetAmountSerializer,
        responses={200: NotifyLowBudgetAmountSerializer}
    )
    def post(self, request, format=None):
        serializer = NotifyLowBudgetAmountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get user data
            user = self.request.user
            notify = serializer.data.get('notify')

            user.notify_low_budget_amount = notify
            user.save()

            result = NotifyLowBudgetAmountSerializer(
                data={
                    'notify': user.notify_low_budget_amount,
                }
            )
            result_payload = result.data if result.is_valid() else {}
            return Response(result_payload, status=status.HTTP_200_OK)
