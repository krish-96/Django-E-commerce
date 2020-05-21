from django.urls import path
from .views import index, contactus, aboutus, search, search_auto, faq

urlpatterns = [
    path("", index, name='index'),
    path("contact-us/", contactus, name='contact-us'),
    path("about-us/", aboutus, name='about-us'),
    path("search/", search, name='search'),
    path("search_auto/", search_auto, name='search-auto'),
    path("faq/", faq, name='search-faq'),
]
