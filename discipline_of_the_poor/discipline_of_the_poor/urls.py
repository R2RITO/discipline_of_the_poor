"""discipline_of_the_poor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from budget.urls import urlpatterns as budget_urls
from dotp_users.urls import urlpatterns as dotp_user_urls
from drf_yasg import openapi


schema_info = openapi.Info(
      title="Discipline of the poor API",
      default_version='v1',
      description="API for everything related to managing budgets.\n"
                  "In order to try the endpoints, you must log in and provide "
                  "a token in the form 'Bearer \\{\\{token\\}\\}'",
      contact=openapi.Contact(email="support@dotp.com"),
)

urlpatterns = []

urlpatterns.extend(budget_urls)
urlpatterns.extend(dotp_user_urls)
