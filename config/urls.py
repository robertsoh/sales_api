from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Final Project ADS')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', schema_view),
    url(r'^api/', include('apps.users.api_v1.urls', namespace='api_users')),
    url(r'^api/', include('apps.products.api_v1.urls', namespace='api_products')),
]
