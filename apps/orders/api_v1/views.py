from django.db import transaction
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.api_v1.serializers import (serialize_item, ItemCartSerializer, OrderUUIDSerializer,
                                            ConfirmOrderSerializer)
from apps.orders.decorators import OrderShippingPriceDecorator
from apps.orders.models import Order


class CartView(APIView):

    def get(self, request):
        order_serializer = OrderUUIDSerializer(data=request.GET)
        order_serializer.is_valid(raise_exception=True)
        current_order = Order.get_or_create_order(order_id=order_serializer.validated_data.get('order_id'))
        items = []
        for item in current_order.items.all():
            items.append(serialize_item(item))
        return Response({
            'data': {
                'id': current_order.id,
                'items': items,
                'total': current_order.total
            }
        })


class AddToCartView(APIView):

    @transaction.atomic
    def post(self, request):
        item_serialize = ItemCartSerializer(data=request.data)
        item_serialize.is_valid(raise_exception=True)
        current_order = item_serialize.validated_data.get('order')
        item = current_order.add_or_update_product(product=item_serialize.validated_data.get('product'),
                                                   quantity=item_serialize.validated_data.get('quantity'))
        return Response({
            'data': serialize_item(item),
            'extra': {
                'cart': {
                    'items_quantity': current_order.items.count()
                },
                'message': '{} was added!'.format(item.product_name)
            }
        })


class ConfirmOrderView(UpdateAPIView):
    serializer_class = ConfirmOrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.confirm_order()
        if instance.has_shipping:
            order_shipping_price = OrderShippingPriceDecorator(instance)
            order_shipping_price.compute_total()
        instance.save()
