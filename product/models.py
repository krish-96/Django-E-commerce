from django.contrib.auth.models import User
from django.db import models
import os
from django.conf import settings
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
class Category(MPTTModel):
    STATUS = {
        ('True','True'),
        ('False','False'),
    }
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(unique=True, null=False,)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
        
    def get_absolute_url(self):
        return reverse('category_products',kwargs={'slug':self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Product(models.Model):
    STATUS = {
        ('True','True'),
        ('False','False'),
    }
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = models.TextField()
    slug = models.SlugField(unique=True, null=False,)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def url(self):
        return os.path.join('/',settings.MEDIA_URL, os.path.basename(str(self.image)))

    # def image_tag(self):
    #
    #     return mark_safe('<img src="{}" width="50" height="50" />'.format(self.url()) )
    #     # return mark_safe(f'<img src="{str(self.image.url)}" width="50" height="50" />')
    # image_tag.short_description = 'Image'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-products',kwargs={'slug':self.slug})

    def averagereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(average=Avg('rate'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('rate'))
        cnt=0
        if reviews['count'] is not None:
            cnt = int(reviews['count'])
        return cnt

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

class Comment(models.Model):
    STATUS = {
            ('New', 'New'),
            ('True', 'True'),
            ('False', 'False'),
        }
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject