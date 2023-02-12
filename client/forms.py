from django import forms
from .models import Client

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('contact_name','company_name','address','country','phone','email','profile')