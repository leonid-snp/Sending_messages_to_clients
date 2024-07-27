from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, UserRegisterForm, UserProfileForm


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class UserProfile(UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user
