from django.forms import ModelForm
from .models import Car, Type
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User



class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=12, required=False)
    email = forms.EmailField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2')
        
 

# class UserUpdateForm(UserChangeForm):
#     first_name = forms.CharField(max_length=50, required=False)
#     last_name = forms.CharField(max_length=50, required=False)
#     phone = forms.CharField(max_length=12, required=False)
#     email = forms.EmailField(max_length=255, required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'phone', 'email')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=12, required=False)
    email = forms.EmailField(max_length=255, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['password'].widget = forms.HiddenInput()  # Hide the password field



class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        
