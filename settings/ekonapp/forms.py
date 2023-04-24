from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
