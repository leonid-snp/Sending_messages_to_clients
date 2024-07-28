from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from . import forms


class UserLoginView(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class UserRegisterView(CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class UserProfile(UpdateView):
    form_class = forms.UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
