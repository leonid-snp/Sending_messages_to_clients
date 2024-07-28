from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm

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


class UserProfileForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name')


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
