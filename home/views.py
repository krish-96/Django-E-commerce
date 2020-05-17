import json

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from product.models import Category, Product, Images, Comment
from .forms import ContactForm, SearchForm
from .models import Setting, ContactMessage

# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[0:4]     # First 4 products
    products_latest = Product.objects.all().order_by('-id')[0:4]     # Last 4 products
    products_picked = Product.objects.all().order_by('?')[0:4]       # Random selected 4 products

    context={
                'setting':setting,
                 'page' : 'home',
                 'category':category,
                 'products_slider':products_slider,
                 'products_latest':products_latest,
                 'products_picked':products_picked
             }
    return render(request, 'index.html', context)

def aboutus(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context={'setting':setting, 'category':category}
    return render(request, 'about.html', context)

def contactus(request):
    # if request.method == 'POST':  # check post
    #     form = CommentForm(request.POST)
    #     print("form object created!")
    #     if form.is_valid():
    #         print("form is valid!")
    #         data = Comment()
    #         data.subject = form.cleaned_data['subject']
    #         data.comment = form.cleaned_data['comment']
    #         data.ip = request.META.get('REMOTE_ADDR')
    #         data.product_id = id
    #         current_user = request.user
    #         data.user_id = current_user.id
    #         data.save()  # save data to table
    #         messages.success(request, "Your review has been sent. Thankyou for your interest.")

    if request.method =='POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(f"{name}:{email}:{subject}:{message}")
        print("form object created!")
        if form.is_valid():
            print("form is valid!")
            form.save()
            messages.success(request, "Your message has been sent. Thankyou for your message.")
            return HttpResponseRedirect('contact-us/')
        else:
            messages.error(request, "Please correct the below errors!")
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm()
    context={'setting':setting, 'form':form, 'category':category }
    return render(request, 'contact.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid==0:
                products = Product.objects.filter(title__icontains=query) # select * FROM product WHER title LIKE '%query%
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()

            context = {
                'category': category,
                'query' : query,
                'products': products,
            }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      product_json = {}
      product_json = rs.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')

    context = {
        'category': category,
        'product': product,
        'images': images,
        'comments': comments,
    }
    return render(request, 'product_detail.html', context)