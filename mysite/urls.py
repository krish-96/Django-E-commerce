"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from home.views import category_products, product_detail
from order.views import shopcart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('product/', include("product.urls")),
    path('order/', include("order.urls")),
    path('user/', include("user.urls")),
    path("category/<int:id>/<slug:slug>/", category_products, name='category-products'),
    path("product/<int:id>/<slug:slug>/", product_detail, name='product-detail'),
    path("shopcart/", shopcart, name='shopcart'),
]

from django.conf import  settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)