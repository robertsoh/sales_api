from django.conf.urls import url

from apps.products.api_v1.views import ProductListCreateAPIView, CategoryListCreateAPIView

urlpatterns = [
    url(r'^categories$', CategoryListCreateAPIView.as_view(), name='categories'),
    url(r'^products$', ProductListCreateAPIView.as_view(), name='products'),
]