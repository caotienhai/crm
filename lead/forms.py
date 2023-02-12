from django import forms
from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status')