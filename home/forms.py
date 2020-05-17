from django.forms import ModelForm, TextInput, EmailInput

from home.models import ContactMessage

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name' : TextInput(attrs={'class':'input', 'placeholder':'Name & Surname', }),
            'subject' : TextInput(attrs={'class':'input', 'placeholder':'Subject', }),
            'email' : TextInput(attrs={'class':'input', 'placeholder':'Email Address',}),
            'message' : TextInput(attrs={'class':'input', 'placeholder':'Your Message', 'rows':5,})
        }

from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()
    catid = forms.IntegerField()