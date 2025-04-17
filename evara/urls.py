"""
URL configuration for evara project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage),

    path('view/<int:p_id>',viewpagefn),
    path('category/<int:ctry_id>',categoryfn),

    path('addproduct/',addproductfn),
    path('editproduct/<int:p_id>',editproductfn),
    path('deleteproduct/<int:p_id>',deleteproductfn),

    path('register/', uregisterfn),
    path('login/',loginfn),
    path('logout',logoutfn),
    path('profile/', profile_view , name='profile_page'),
     
    path('wishlist/', wishlist_view, name='wishlist_page'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),

    path('payment/success/dummy', payment_success, name='payment_success'),

    path('blog',blogfn),
    path('search',searchfn),
    path('contact',contact),

   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)