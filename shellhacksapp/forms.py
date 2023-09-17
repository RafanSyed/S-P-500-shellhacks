from django import forms
from .models import Company
from django.forms import ModelForm
from .models import *


class CompanySearchForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']  
