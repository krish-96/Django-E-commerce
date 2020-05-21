from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile

@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user     # Access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'profile': profile, 'category': category}
    return render(request, 'user_profile.html', context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            messages.success(request, f"Welcome {username}")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Useername or Password is incorrect.")
            return HttpResponseRedirect('/')
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category}
    return render(request, 'login_form.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_form(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    category = Category.objects.all()
    form = SignUpForm()
    context = { 'category': category, 'form': form}
    return render(request, 'signup_form.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user data
        # *"instance=request.user.userprofile" comes from "userprofile" model --> OneToOne relationship
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated!")
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, user_form.errors, profile_form.errors)
            return HttpResponseRedirect('/user/update')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)  # "userprofile" model --> OneToOne relationship with user
        context = {
                   'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form,
                }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)      # important!!
            messages.success(request, "Your password was successfully updated!")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, f"Please correct the error below. <br> {form.errors}")
            return HttpResponseRedirect('/user/password')
    form = PasswordChangeForm(request.user)
    category = Category.objects.all()
    context = {
            'category': category,
            'form': form,
        }
    return render(request, 'user_password.html', context)

@login_required(login_url='/login')
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
            'category': category,
            'orders': orders,
        }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
            'category': category,
            'order': order,
            'orderitems': orderitems,
        }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    context = {
            'category': category,
            'order_product': order_product,
        }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login')
def user_order_product_detail(request, id, oid):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request,id):
    current_user = request.user  # Access user session information
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Your comment deleted!")
    return HttpResponseRedirect('/user')
