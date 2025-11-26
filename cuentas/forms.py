from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Heredamos de UserCreationForm que ya es un ModelForm
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] # Agregamos email si quieres