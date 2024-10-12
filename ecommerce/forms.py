from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Products, RegisterUser

class Producatform(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'desc', 'price', 'img'] 
        
        def clean(self):
            name = self.cleaned_data.get('name')
            if Products.objects.filter(name=name).exists():
                raise forms.ValidationError("product already exists")
            return name
        
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = '__all__'

