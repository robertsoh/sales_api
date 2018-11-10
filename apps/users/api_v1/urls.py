from django.conf.urls import url
from rest_framework.authtoken import views

from apps.users.api_v1.views import UsersCreateAPIView

urlpatterns = [
    url(r'^register$', UsersCreateAPIView.as_view(), name='register_user'),
    url(r'^login$', views.obtain_auth_token, name='login'),
]