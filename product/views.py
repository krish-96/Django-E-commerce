from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

from home.models import Setting
from product.forms import CommentForm
from product.models import Product, Comment, Category


def index(request):
    return HttpResponse('This is products page!')

def comment(request, id):
    url = request.META.get('HTTP_REFERER')  #get last url
    # return HttpResponse(url)
    if request.method =='POST':     #check post
        form = CommentForm(request.POST)
        print("form object created!")
        if form.is_valid():
            print("form is valid!")
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()     #save data to table
            messages.success(request, "Your review has been sent. Thankyou for your interest.")
            return HttpResponseRedirect(url)


        return HttpResponseRedirect(url)

