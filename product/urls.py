from django.urls import path
from .views import index, comment

urlpatterns = [
    path("", index, name='product-index'),
    path("addcomment/<int:id>/", comment, name='addcomment'),

]

