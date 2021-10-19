import collections
from rest_framework import serializers
from decimal import Decimal

from rest_framework.relations import HyperlinkedRelatedField
from store.models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = serializers.StringRelatedField()
    #collection = serializers.PrimaryKeyRelatedField(
    #    queryset=Collection.objects.all()
    #)
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.special_field = validated_data.get('unit_price') + 'etc'
    #     instance.save()
    #     return instance