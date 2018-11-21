from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.orders.models import Item


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
