from django.contrib.auth import models
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import tree
from django.views.generic import ListView, CreateView
from .models import Order, OrderItem, Product, Contact_Info, Service, ShippingAddress
from django.http import JsonResponse
from .utils import cartData, cookieCart, guessOrder
import json
import datetime


# Create your views here.
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/home.html', context)


def booking(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/booking.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guessOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)


def service(request):
    data = cartData(request)
    cartItems = data['cartItems']

    allservices = Service.objects.all()
    context = {
        'cartItems': cartItems, 'allservices': allservices}

    return render(request, 'store/service_list.html', context)

# class ServiceListView(ListView):
#     model = Service
#     allservices = Service.objects.all()
#     template_name = 'store/service_list.html'
#     context_object_name = 'service_list'


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def order(request):
    return render(request, 'store/order.html')

# def contact(request):
#     return render(request, 'store/contact.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Contact_Info
    template_name = 'store/contact.html'
    context_object_name = 'posts'
    fields = ['first_name', 'last_name', 'email', 'phone', 'message']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
