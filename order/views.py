import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from product.models import Category
from .models import ShopCart
from .forms import ShopCartForm

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