import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common import constants
from apps.common.models import TimeStampedModel


class Order(TimeStampedModel):

    STATUS_DRAFT = 'draft'
    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    STATUS_CANCELED = 'canceled'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_NEW, 'New'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered')
    )

    CART_KEY = 'cart_key'
    SEQUENCE_CODE = 'orders'

    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    number = models.PositiveIntegerField('Number', null=True, editable=False)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    subtotal = models.DecimalField('Subtotal', editable=False, default=0, decimal_places=settings.DECIMAL_PLACES,
                                   max_digits=settings.MAX_DIGITS)
    shipping = models.DecimalField('Shipping', editable=False, default=0, decimal_places=settings.DECIMAL_PLACES,
                                   max_digits=settings.MAX_DIGITS)
    total = models.DecimalField('Total', editable=False, default=0, decimal_places=settings.DECIMAL_PLACES,
                                max_digits=settings.MAX_DIGITS)

    registration_date = models.DateTimeField('Registration date', null=True, blank=True)
    cancelation_date = models.DateTimeField('Cancelation date', null=True, blank=True)
    payment_date = models.DateTimeField('Payment date', null=True, blank=True)
    shipping_date = models.DateTimeField('Shipping date', null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        default_related_name = 'orders'

    def __str__(self):
        return str(self.id)

    def compute_total(self):
        self.subtotal = sum(map(lambda x: x.total, self.items.all()))
        self.shipping = constants.DEFAULT_SHIPPING_COST
        self.total = self.subtotal + self.shipping

    @property
    def get_number_display(self):
        return str(self.number).zfill(8)

    def add_or_update_product(self, product, quantity=1):
        current_item = self.items.filter(product=product).first()
        if current_item is not None:
            current_item.quantity += quantity
            current_item.save()
            return current_item
        else:
            return Item.objects.create(
                order=self,
                product=product,
                unit_price=product.price,
                quantity=quantity
            )

    @classmethod
    def get_or_create_order(cls, order_id):
        order, created = cls.objects.get_or_create(id=order_id)
        return order

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = self.STATUS_NEW
            self.registration_date = timezone.now()
            self.number = self.generate_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_number(cls):
        from apps.sequences.models import Sequence
        return Sequence.get_next_value(cls.SEQUENCE_CODE)


class Item(TimeStampedModel):

    order = models.ForeignKey('Order', related_name='items')
    product = models.ForeignKey('products.Product', related_name='items', null=True, on_delete=models.SET_NULL)

    product_name = models.CharField('Product name', max_length=100, editable=False)
    unit_price = models.DecimalField('Unite price', decimal_places=settings.DECIMAL_PLACES,
                                     max_digits=settings.MAX_DIGITS)
    quantity = models.PositiveSmallIntegerField('Quantity')
    subtotal = models.DecimalField('Subtotal', editable=False, decimal_places=settings.DECIMAL_PLACES,
                                   max_digits=settings.MAX_DIGITS)
    total = models.DecimalField('Total', editable=False, decimal_places=settings.DECIMAL_PLACES,
                                max_digits=settings.MAX_DIGITS)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return '{} {}'.format(self.product_name, self.total)

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
        self._compute_total()
        super().save(*args, **kwargs)

    def _compute_total(self):
        self.subtotal = self.quantity * self.unit_price
        self.total = self.subtotal
