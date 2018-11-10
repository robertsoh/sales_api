from rest_framework.generics import ListCreateAPIView

from apps.products.api_v1.serializers import CategorySerializer, ProductSerializer
from apps.products.models import Category, Product


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
