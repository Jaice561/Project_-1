from . import views
from django.urls import path
from.views import PostCreateView, processOrder


urlpatterns = [
    path('', views.home, name='store-home'),
    path('service_list/', views.service, name='store-service_list'),
    path('about/', views.about, name='store-about'),
    # path('contact/', views.contact, name='store-contact'),
    path('post/new/', PostCreateView.as_view(), name='store-contact'),
    path('booking/', views.booking, name='store-booking'),
    path('checkout/', views.checkout, name='store-checkout'),
    path('cart/', views.cart, name='store-cart'),
    path('booking/update_item/', views.updateItem, name="update_item"),
    path('cart/update_item/', views.updateItem, name="update_item"),
    path('checkout/process_order/', views.processOrder, name="process_order")
]
