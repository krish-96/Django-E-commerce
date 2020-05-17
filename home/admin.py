from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'mail', 'status']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']

admin.site.register(Setting, SettingsAdmin)
admin.site.register(ContactMessage, ContactAdmin)