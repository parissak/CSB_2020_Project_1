from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True,label='Username', min_length=3)
    email = forms.EmailField(required=True,label='Email', min_length=3)
    password1 = forms.CharField(required=True,label='Password', min_length=3)
    password2 = None

    class Meta:
        model=User
        fields = ('username', 'email', 'password1')