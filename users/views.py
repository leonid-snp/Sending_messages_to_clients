from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from . import forms
from .models import User


class UserLoginView(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class UserRegisterView(CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class UserProfile(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = forms.UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    permission_required = 'users.view_user'
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Восстановление пароля'}


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:list')
    extra_context = {'title': 'Профиль'}

    def get_form_class(self):
        user = self.request.user
        if self.object.email == user.email:
            return forms.UserProfileForm
        if user.has_perm('users.cam_change_user'):
            return forms.UserModerProfileForm


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:list')
    extra_context = {'title': 'Удаление профиля'}


class UserListView(LoginRequiredMixin, ListView):
    model = User
    extra_context = {'title': 'Список пользователей'}
