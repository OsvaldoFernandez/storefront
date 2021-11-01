from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import Order, Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer, UpdateCartItemSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #filterset_fields = ['collection_id', 'unit_price'] SOLO PARA FILTRAR EXACTOS
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description'] # Se puede agregar 'collection__title'
    ordering_fields = ['unit_price', 'last_update']
    

    # def get_queryset(self): THIS IS FOR CUSTOM FILTERING
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None: 
    #         queryset = queryset.filter(collection_id=collection_id)
        
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because its associated with an order'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)

    # overridear get_queryset(self) y get_serializer_class(self) para cosas más complejas

class CollectionViewSet(ModelViewSet): # Alternative: ReadOnlyModelViewSet 
    queryset = Collection.objects.annotate(products_count=Count('product'))
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because its associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return { 'product_id': self.kwargs['product_pk'] }

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    # PREFETCH DEL PREFETCHED
    queryset = Cart.objects.prefetch_related('items__product').all() 

    def get_serializer_context(self):
        return {'request': self.request}

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return { 'cart_id': self.kwargs['cart_pk'] }

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])