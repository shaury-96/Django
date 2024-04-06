from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import CustomUser

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md bd', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md bd', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-white border-left-0 border-md bd', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'form-control bg-white border-md border-left-0 pl-3 bd', 'placeholder': 'Phone Number', 'type': 'tel'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-white border-left-0 border-md bd', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-white border-left-0 border-md bd', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model=CustomUser
        fields=['email','first_name', 'last_name', 'phone_number', 'password1', 'password2']