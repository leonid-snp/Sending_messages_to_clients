from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from newsletter.form import StyleFormMixin
from users.models import User


class LoginUserForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
