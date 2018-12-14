## Configuración de variables de entorno para el sistema:

```
    DJANGO_SETTINGS_MODULE=config.settings.dev
    DB_PORT
    DB_USER
    ALLOWED_HOSTS
    SECRET_KEY
    DB_NAME
    DB_HOST
    DB_PASSWORD
    MINIO_STORAGE_ENDPOINT
    MINIO_STORAGE_ACCESS_KEY
    MINIO_STORAGE_SECRET_KEY
    MINIO_STORAGE_MEDIA_BUCKET_NAME
    EMAIL_HOST=smtp.mailgun.org
    EMAIL_HOST_PASSWORD
    EMAIL_HOST_USER
    EMAIL_PORT
    EMAIL_USE_TLS
    CELERY_BROKER_URL
    DEFAULT_FROM_EMAIL
    DSN_URL
```

## Patrones agregados:


- `Unit of Work` en `apps/orders/api_v1/views.py`

```python
from django.db import transaction

class AddToCartView(APIView):

    @transaction.atomic
    def post(self, request):
        pass
```

- `DTO` en `apps/orders/api_v1/serializers.py`

```python
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
```


- `Ǹotification pattern` en `apps/products/api_v1/serializers.py`

```python

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'active', 'price', 'short_description', 'long_description', 'image',)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('The price is negative')
        return value
```

- `Database migrations` en `apps/products/migrations/0001_initial.py`

```python

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('complete_name', models.CharField(editable=False, max_length=200, null=True)),
                ('slug', models.SlugField(editable=False, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/images/%Y/%m/%d/')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.Category')),
            ],
            )
    ]
```

- `Observer pattern` en `apps/orders/signals.py`
   
    Al agregar un Item a la Orden se actualiza el total de la Orden automáticamente
   
```python
@receiver(post_save, sender=Item)
def post_save_item(sender, instance, **kwargs):
    instance.order.compute_total()
    instance.order.save()
```

- `Command pattern` en `apps/orders/api_v1/views.py`

    Encapsula el request en un objeto `request` que puede ser accedido y manipulado.

```python
class AddToCartView(APIView):

    def post(self, request):
        item_serialize = ItemCartSerializer(data=request.data)
```

- `Template method pattern` en `apps/products/api_v1/views.py`

    Django utiliza este patrón en las vistas genéricas basadas en clase para evitar repetir código y define métodos
    como `GET`, `POST`, `PUT`, etc. que pueden ser sobrescritos.

```python
from rest_framework.generics import ListCreateAPIView


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer

```


- `Decorator pattern` en `apps/orders/decorators.py`

    Utilizado para calcular el total de la orden según tenga o no envío.

```python

class IOrder(models.Model):

    class Meta:
        abstract = True

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


class Order(TimeStampedModel, IOrder):
    
    def compute_total(self):
        self.subtotal = sum(map(lambda x: x.total, self.items.all()))
        self.total = self.subtotal


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
```
