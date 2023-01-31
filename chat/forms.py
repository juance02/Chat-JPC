from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from chat.models import *


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields=['username','password1','password2']
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username']
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
        }

class PerfilUpdateForm(forms.ModelForm):
     class Meta:
        model = perfil
        fields = ['image', 'descripcion']
        widgets = {
            #'image': fi(attrs={'class':'form-control'}),
            'descripcion': TextInput(attrs={'class':'form-control'}),
        }