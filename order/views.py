import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string

from product.models import Category, Product
from user.models import UserProfile
from .models import ShopCart, OrderProduct, Order
from .forms import ShopCartForm, OrderForm


# Create your views here.
def index(request):
    return HttpResponse("Order Page")

@login_required(login_url='/login')  # check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Accessing user session information

    # return HttpResponse(url)
    checkproduct = ShopCart.objects.filter(product_id=id)  # check product in shopcart
    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        print(form)
        print("form object created!")
        if form.is_valid():
            print("form is valid!")
            if control == 1: # Update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Insert to ShopCart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart!.")
        return HttpResponseRedirect(url)

    else : # if there is no post
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:  # insert to ShopCart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart.")
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    context = {
        'category':category,
        'shopcart':shopcart,
        'total':total,
        }
    return render(request, 'shopcart_products.html', context)

@login_required(login_url='/login')  # check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from the cart.")
    return HttpResponseRedirect('/shopcart')

def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == "POST":
        form = OrderForm(request.POST)
        print("form is created!")
        #return HttpRespionse(request.POST.items())
        if form.is_valid():
            print("form is Valid!")
            # Send Credit Card to bank and get result if bank Response ok continue, if not, Show the error
            # ---------------------
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get("REMOTE_ADDR")
            ordercode = get_random_string(5).upper() # Random cod
            data.code = ordercode
            data.save()

            # Move Shopcart items to Order Products items
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id   # Order Id
                detail.product_id = rs.product_id
                detail.user_id = rs.user_id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                #   *** Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                # ***********************

            ShopCart.objects.filter(user_id=current_user.id).delete()   # Clear & Delete Shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you")
            return render(request, "order_completed.html", {'ordercode':ordercode, 'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    context = {
        'category': category,
        'shopcart': shopcart,
        'profile': profile,
        'total': total,
        }
    return render(request, 'order_form.html', context)