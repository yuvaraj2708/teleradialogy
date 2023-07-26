from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.forms import PasswordResetForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']



class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, name):
        return CustomUser.objects.filter(name__iexact=name, is_active=True)
