from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet, basename='carts')
router.register('collections', views.CollectionViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(products_router.urls)),
    path(r'', include(carts_router.urls))
    # path('collections', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail')
]