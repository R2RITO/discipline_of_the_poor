"""
DotpUsers app urls
"""
from django.conf.urls import url
from django.urls import include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from dotp_users.views.dotp_user_view import DotpUserViewSet


router = routers.DefaultRouter()
router.register(r'register', DotpUserViewSet)

urlpatterns = [
    url(r'dotp_auth/', include(router.urls)),
    url(r'dotp_auth/token',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    url(r'dotp_auth/refresh',
        TokenRefreshView.as_view(),
        name='token_refresh_view'),
]
