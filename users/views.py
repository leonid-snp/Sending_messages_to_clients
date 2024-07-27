from django.contrib.auth.views import LoginView

from users.forms import LoginUserForm


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


