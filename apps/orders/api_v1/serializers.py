from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.orders.models import Item, Order


def serialize_item(item):
    data = {
        'order': item.order.id,
        'item': item.id,
        'product_name': item.product_name,
        'unit_price': item.unit_price,
        'quantity': item.quantity,
        'total': item.total,
        'product_url': reverse('api_products:product-detail', kwargs={'pk': item.product.id})
    }
    return data


class OrderUUIDSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=False)


class ItemCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('product', 'quantity', 'order',)


class ConfirmOrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(decimal_places=settings.DECIMAL_PLACES, max_digits=settings.MAX_DIGITS,
                                     read_only=True)
    shipping = serializers.DecimalField(decimal_places=settings.DECIMAL_PLACES, max_digits=settings.MAX_DIGITS,
                                        read_only=True)
    subtotal = serializers.DecimalField(decimal_places=settings.DECIMAL_PLACES, max_digits=settings.MAX_DIGITS,
                                        read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'has_shipping', 'full_name', 'email', 'phone', 'street', 'city', 'subtotal', 'total',
                  'shipping',)
