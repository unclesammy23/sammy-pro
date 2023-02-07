
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import requests


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('store')



    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username Or password does not exist')


    context={'page':page}
    return render(request,'store/login_register.html',context)

def LogoutUser(request):
    logout(request)
    return redirect('store')



def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request,'an error occure during registration')




    return render(request, 'store/login_register.html',{'form':form})




def store(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = None

        if customer:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            total_quantity = 0
            for item in items:
             total_quantity += item.quantity

        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order,'total_quantity':total_quantity}
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    
     if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
     else:
        items = []
        order ={'get_cart_total':0, 'get_cart_items':0}

    

     context ={'items':items, 'order':order}
     return render(request, 'store/checkout.html', context)



@login_required(login_url='login')
def add_to_cart(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=item)
        if not created:
            order_item.quantity += 1
            order_item.save()
    return redirect('cart')



@login_required(login_url='login')
def remove_from_cart(request, pk):
    item = OrderItem.objects.filter(pk=pk).first()
    if item:
        item.delete()
    return redirect('cart')

@login_required(login_url='login')
def update_cart(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.quantity = request.POST.get('quantity')
    item.save()
    return redirect('cart')


def view_product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/view_product.html', {'product': product})






def place_order(request):
    order = Order.objects.get(pk=request.session['order_id'])
    paypal_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypal_email = "your-sandbox-merchant-email-here"
    return_url = "http://localhost:8000/process-payment"
    cancel_return = "http://localhost:8000/cancel"
    item_name = "Order " + str(order.id)
    item_amount = order.get_cart_total
    custom = "Order " + str(order.id)

    if request.method == "POST":
        requests.post(paypal_url, {
            "cmd": "_xclick",
            "business": paypal_email,
            "return": return_url,
            "cancel_return": cancel_return,
            "amount": item_amount,
            "item_name": item_name,
            "custom": custom,
        })
        return redirect("/process-payment")

    context = {
        "order": order,
        "paypal_url": paypal_url,
        "paypal_email": paypal_email,
        "return_url": return_url,
        "cancel_return": cancel_return,
        "item_name": item_name,
        "item_amount": item_amount,
        "custom": custom,
    }

    return render(request, "place_order.html", context)
