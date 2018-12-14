from rest_framework import serializers

from apps.products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'active', 'price', 'short_description', 'long_description', 'image',)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('The price is negative')
        return value
