from django.urls import path
from .views import index, addtoshopcart, deletefromcart, orderproduct

urlpatterns = [
    path("", index, name='order-index'),
    path("addtoshopcart/<int:id>/", addtoshopcart, name='addtoshopcart'),
    path("deletefromcart/<int:id>/", deletefromcart, name='deletefromcart'),
    path("orderproduct/", orderproduct, name='orderproduct'),
]
