from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.common.models import TimeStampedModel
from apps.products.querysets import ProductQuerySet


class Category(TimeStampedModel):

    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

    name = models.CharField('Name', max_length=100)
    complete_name = models.CharField(max_length=200, null=True, editable=False)
    slug = models.SlugField(max_length=255, editable=False, null=True)

    image = models.ImageField(upload_to='category/images/%Y/%m/%d/', null=True, blank=True)
    description = models.CharField('Description', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.complete_name or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self._compute_complete_name()
        super().save(*args, **kwargs)

    def _compute_complete_name(self):
        names = [self.name]
        category = self.parent
        while category is not None:
            names.append(category.name)
            category = category.parent
        self.complete_name = ' / '.join(reversed(names))


class Product(TimeStampedModel):
    category = models.ForeignKey('Category', related_name='products')
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField(max_length=255, editable=False)
    active = models.BooleanField('Active', default=True)
    price = models.DecimalField('Price', decimal_places=settings.DECIMAL_PLACES, max_digits=settings.MAX_DIGITS)
    short_description = models.TextField('Description')
    long_description = models.TextField('Long Description', null=True, blank=True)
    has_stock = models.BooleanField('Has stock?', default=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        return self.images.first()


class ProductImage(TimeStampedModel):

    product = models.ForeignKey('Product', related_name='images')
    file = models.ImageField(upload_to='product/images/%Y/%m/%d/')
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ('order',)

    def __str__(self):
        return '{}-{}'.format(self.product.name, self.order)
