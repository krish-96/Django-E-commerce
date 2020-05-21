from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage, FAQ


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'mail', 'status']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']
 
class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'answer', 'status']
    list_filter = ['status']


admin.site.register(Setting, SettingsAdmin)
admin.site.register(ContactMessage, ContactAdmin)
admin.site.register(FAQ, FAQAdmin)