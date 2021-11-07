import collections
from rest_framework import serializers
from decimal import Decimal
from rest_framework.fields import ReadOnlyField

from rest_framework.relations import HyperlinkedRelatedField, PrimaryKeyRelatedField
from store.models import Customer, Product, Collection, Review, Cart, CartItem

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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']
    
    product = SimpleProductSerializer(read_only=True)

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta: 
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        try: 
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CartItem
        fields = ['quantity']

class CartSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cart
        fields = ['id', 'items', 'total_price']

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
