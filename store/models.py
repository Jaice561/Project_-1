from django.db import models
from django.db.models.aggregates import Max
from django.db.models.expressions import F
from django.shortcuts import redirect
from django.urls import reverse
from django.urls.conf import path
from django.contrib.auth.models import User


# Create your models here.

# class Collection(models.Model):
#     title = models.CharField(max_length=255)
#     featured_product = models.ForeignKey(
#         'Product', on_delete=models.SET_NULL, null=True, related_name='+')


# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     inventory = models.IntegerField()
#     last_update = models.DateTimeField(auto_now=True)
#     collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, default='')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    placed_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    placed_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# class Customer(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=255)
#     birth_date = models.DateField(null=True)


# class Order(models.Model):
#     PAYMENT_STATUS_PENDING = 'P'
#     PAYMENT_STATUS_COMPLETE = 'C'
#     PAYMENT_STATUS_FAILED = 'F'
#     PAYMENT_STATUS_CHOICES = [
#         (PAYMENT_STATUS_PENDING, 'Pending'),
#         (PAYMENT_STATUS_COMPLETE, 'Complete'),
#         (PAYMENT_STATUS_FAILED, 'Failed')
#     ]

#     placed_at = models.DateTimeField(auto_now_add=True)
#     payment_status = models.CharField(
#         max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
#     customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     quantity = models.PositiveSmallIntegerField()
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# class Cart(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField()


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=250, null=False)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Contact_Info(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('store-contact')


# class Service(models.Model):
#     service_name = models.CharField(max_length=255)
#     service_price = models.DecimalField(max_digits=5, decimal_places=2)
#     service_time = models.CharField(max_length=255)

#     def __str__(self):
#         return self.service_name
