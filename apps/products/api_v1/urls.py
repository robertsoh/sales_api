from django.conf.urls import url

from apps.products.api_v1.views import ProductListCreateAPIView, CategoryListCreateAPIView, ProductDetailAPIView

urlpatterns = [
    url(r'^categories$', CategoryListCreateAPIView.as_view(), name='categories'),
    url(r'^products$', ProductListCreateAPIView.as_view(), name='products'),
    url(r'^products/(?P<pk>[\d]+)/$', ProductDetailAPIView.as_view(), name='product-detail'),
]