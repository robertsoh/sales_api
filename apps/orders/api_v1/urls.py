from django.conf.urls import url

from apps.orders.api_v1.views import CartView, AddToCartView, ConfirmOrderView

urlpatterns = [
    url(r'^orders/cart$', CartView.as_view(), name='cart'),
    url(r'^orders/add-to-cart$', AddToCartView.as_view(), name='add_to_cart'),
    url(r'^orders/(?P<pk>[\w-]{36})/confirm', ConfirmOrderView.as_view(), name='pay_order')
]
