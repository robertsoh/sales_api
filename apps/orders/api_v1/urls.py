from django.conf.urls import url

from apps.orders.api_v1.views import CartView, AddToCartView

urlpatterns = [
    url(r'^cart$', CartView.as_view(), name='cart'),
    url(r'^add-to-cart$', AddToCartView.as_view(), name='add_to_cart'),
]