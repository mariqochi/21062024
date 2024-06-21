from django.forms import ModelForm
from .models import Car, Type, Booking
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
        


from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'loc_from', 'loc_to']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date must be after start date.")

        return cleaned_data