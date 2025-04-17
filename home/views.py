from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product, Category, Profile, Comment, Blog
from .forms import *
from django.db.models import Q
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def frontpage(request):

    y=Category.objects.all()   

    p=request.GET.get('pag')
    print(p)

    a=Product.objects.all()
    b=Paginator(a,8)
    x=b.get_page(p)

    return render (request, 'home.html' ,{'xyz':x,'cat':y})

def viewpagefn(request,p_id):  

    if request.method =='POST':
        f=CommentForm(request.POST)
        if f.is_valid():
            x=f.save(commit=False)
            x.us=request.user
            a=Product.objects.get(id=p_id)
            x.post=a
            x.save()
            return redirect('/')
    else:
        f=CommentForm()
        a=Product.objects.get(id=p_id)
        c=Comment.objects.filter(post=p_id)
        return render (request, 'viewpage.html',{'abc':a, 'fm':f , 'cmt':c})

def categoryfn(request,ctry_id): 
    x=Product.objects.filter(ctry=ctry_id)
    y=Category.objects.all()
    return render (request, 'home.html',{'xyz':x, 'cat':y })

def searchfn(request):
    a=request.GET['s']
    # print(a)
    x=Product.objects.filter(Q(title__icontains=a)| Q(details__icontains=a))
    y=Category.objects.all() 
    return render (request, 'home.html',{'xyz':x, 'cat':y})

def contact(request):
    return render (request, 'contact.html')


# ==============blog============================
def blogfn(request):

    bl=Blog.objects.all()
    return render (request, 'blog.html',{'xyz':bl})


# ============================================
def addproductfn(request):
        if request.method=='POST':
            f=ProductForm(request.POST,request.FILES)
            if f.is_valid():
                x=f.save(commit=False)
                x.us=request.user
                x.save()
                # f.save()
                return redirect('/')
        else:
            f=ProductForm()
            return render(request,'addproduct.html',{'form':f,'x':'Add'})



def editproductfn(request,p_id):
    b=Product.objects.get(id=p_id)
    print(b.us,'----',request.user)
    if b.us==request.user:
        if request.method=='POST':
            b=Product.objects.get(id=p_id)
            f=ProductForm(request.POST,request.FILES,instance=b)
            if f.is_valid():
                f.save()
                return redirect('/')
                    
        else:
            b=Product.objects.get(id=p_id)
            f=ProductForm(instance=b)
            return render(request,'addproduct.html',{'form':f,'x':'Edit'})
    else:
        return redirect('/')
    

def deleteproductfn(request,p_id):
    x=Product.objects.get(id=p_id)
    x.delete()
    return redirect('/')
# =================================================

def uregisterfn(request):
    if request.method=='POST':
        u=request.POST['uname']
        e=request.POST['email']
        f=request.POST['full_name']
        p=request.POST['password']
        c=request.POST['cpassword']
        if (p==c):
            if User.objects.filter(username=u).exists():
                return render (request, 'register.html',{'er':'Username exists!!!'})
                  
            elif User.objects.filter(email=e).exists():
                return render (request, 'register.html',{'er':'e-mail exists!!!'})
            else:
                User.objects.create_user(username=u,email=e,first_name=f, last_name='user',password=p)
                return redirect('/login')
        else:
             return render (request, 'register.html',{'er':'Password incorrect!!!'})
    else:
        return render (request, 'register.html')


def loginfn(request):
    if request.method=='POST':
     u=request.POST['uname']
     p=request.POST['password']
     x=auth.authenticate(username=u, password=p,last_name='user')
     if x:
        auth.login(request,x)
        return redirect('/profile')
     else:
        return render (request, 'login.html',{'er':'invalid username or password'})
    else:
        return render (request, 'login.html')



def logoutfn(request):
    auth.logout(request)
    return redirect('/login')


# ============================================

@login_required(login_url='/login')
def profile_view(request):
    # Try to get the user's profile; if not found, show a message
    try:
        profile = Profile.objects.get(us=request.user)  
    except Profile.DoesNotExist:
        profile = None  # No profile found

    if request.method == "POST":
        if profile:
            form = ProfileForm(request.POST, instance=profile)
        else:
            form = ProfileForm(request.POST)  # Create new profile

        if form.is_valid():
            profile = form.save(commit=False)
            profile.us = request.user  # Assign the logged-in user to the profile
            profile.save()
            return redirect('profile_page')

    else:
        form = ProfileForm(instance=profile) if profile else ProfileForm()

    return render(request, 'profile.html', {'form': form, 'profile': profile,})


# =================wishlist=========================

from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Wishlist


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(us=request.user, product=product)

    if not created:
        messages.info(request, "Already in wishlist.")
    else:
        messages.success(request, "Added to wishlist.")
    return redirect('wishlist_page')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(us=request.user, product=product).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist_page')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(us=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# ====================cart========================================

from .models import  Cart
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(us=request.user, product=product)  

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')  # Redirect to cart page

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(us=request.user) 
    total_price = sum(item.product.amount * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

    # Razorpay client setup
    # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # payment = client.order.create({
    #     'amount': int(total_price * 100),  # Convert to paise
    #     'currency': 'INR',
    #     'payment_capture': '1'
    # })

    # return render(request, 'cart.html', {
    #     'cart_items': cart_items,
    #     'total_price': total_price,
    #     'payment': payment,
    #     'razorpay_key_id': settings.RAZORPAY_KEY_ID
    # })



@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, us=request.user)  
    cart_item.delete()
    return redirect('cart_view')


# ===============================================================================

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_success(request):
    Cart.objects.filter(us=request.user).delete() # Clear cart after payment
    return render(request, 'success.html')
