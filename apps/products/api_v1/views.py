from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.api_v1.serializers import CategorySerializer, ProductSerializer
from apps.products.models import Category, Product


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailAPIView(APIView):

    def get(self, request, pk):
        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance)
        return Response(serializer.data)
