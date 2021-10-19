from django.core import exceptions
from django.db.models import query
from django.db.models.aggregates import Count, Max, Min, Avg
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db import transaction
from store.models import Product, Customer, Collection, Order, OrderItem
from django.contrib.contenttypes.models import ContentType
from tags.models import  TaggedItem
from django.conf import settings


# Create your views here.

def say_hello(request):
    # with transaction.atomic():
    #     new_order = Order()
    #     new_order.customer_id = 1
    #     new_order.save()

    #     item = OrderItem()
    #     item.order = new_order
    #     item.product_id = -1
    #     item.quantity = 1 
    #     item.unit_price = 10
    #     item.save()

    return render(request, 'hello.html', {'name': 'uva'})
