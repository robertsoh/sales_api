import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedModel
from apps.orders import exceptions, tasks
from apps.orders.decorators import IOrder


class Order(TimeStampedModel, IOrder):

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
    has_shipping = models.BooleanField(default=False)
    shipping = models.DecimalField('Shipping', editable=False, default=0, decimal_places=settings.DECIMAL_PLACES,
                                   max_digits=settings.MAX_DIGITS)
    total = models.DecimalField('Total', editable=False, default=0, decimal_places=settings.DECIMAL_PLACES,
                                max_digits=settings.MAX_DIGITS)

    registration_date = models.DateTimeField('Registration date', null=True, blank=True)
    cancelation_date = models.DateTimeField('Cancelation date', null=True, blank=True)
    payment_date = models.DateTimeField('Payment date', null=True, blank=True)
    shipping_date = models.DateTimeField('Shipping date', null=True, blank=True)

    full_name = models.CharField('Full name', max_length=255, null=True)
    email = models.EmailField('Email', null=True)
    phone = models.CharField('Phone', max_length=20, null=True)
    street = models.CharField('Address', max_length=255, null=True)
    city = models.CharField('City', max_length=255, null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        default_related_name = 'orders'

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = self.STATUS_DRAFT
            self.registration_date = timezone.now()
            self.number = self.generate_number()
        super().save(*args, **kwargs)

    @property
    def get_number_display(self):
        return str(self.number).zfill(8)

    @classmethod
    def get_or_create_order(cls, order_id):
        order, created = cls.objects.get_or_create(id=order_id)
        return order

    @classmethod
    def generate_number(cls):
        from apps.sequences.models import Sequence
        return Sequence.get_next_value(cls.SEQUENCE_CODE)

    def _check_status(self, status):
        if self.status != status:
            raise exceptions.InvalidStatusChangeException

    def compute_total(self):
        self.subtotal = sum(map(lambda x: x.total, self.items.all()))
        self.total = self.subtotal

    def confirm_order(self):
        # self._check_status(self.STATUS_DRAFT)
        self.compute_total()
        self.status = self.STATUS_NEW
        self.payment_date = timezone.now()
        self.save()
        tasks.send_order_confirmation.delay(self.id)

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
