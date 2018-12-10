from abc import abstractmethod

from django.db import models
from apps.common import constants


class IOrder(models.Model):

    class Meta:
        abstract = True

    @abstractmethod
    def compute_total(self):
        pass


class IOrderDecorator(IOrder):

    class Meta:
        abstract = True

    def __init__(self, order):
        super().__init__()
        self._order = order

    @abstractmethod
    def compute_total(self):
        pass


class OrderShippingPriceDecorator(IOrderDecorator):

    class Meta:
        abstract = True

    def compute_total(self):
        subtotal = self._order.total
        self._order.shipping = constants.DEFAULT_SHIPPING_COST
        self._order.total = subtotal + self._order.shipping
