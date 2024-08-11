import random

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from newsletter.forms import (ClientForm, CreateNewsletterForm, MessageForm,
                              UpdateModerNewsletterForm, UpdateNewsletterForm)
from newsletter.models import Client, HistoryNewsletter, Message, Newsletter
from newsletter.services import get_blogs_from_cache


class HomeTemplateView(TemplateView):
    """
    Класс отображения главной страницы.
    """
    template_name = 'newsletter/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        """
        Переопределяем функцию для отображения
        данных о рассылках и блоге.
        """
        blog = list(get_blogs_from_cache())
        unique_client = Client.objects.all().distinct('email').count()
        random_blog = set()
        while len(random_blog) != 3:
            random_blog.add(random.choice(blog))
        activ_newsletter = Newsletter.objects.filter(status='LA').count()
        count_newsletter = Newsletter.objects.all().count()
        data = {
            'count_newsletter': count_newsletter,
            'activ_newsletter': activ_newsletter,
            'unique_clients': unique_client,
            'blog_articles': random_blog
        }

        return super().get_context_data(**data)


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс отображения страницы создания сообщения.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message-list')
    permission_required = 'newsletter.can_add_message'
    extra_context = {'title': 'Создать сообщение'}

    def form_valid(self, form):
        """
        Переопределяем функцию для присваивания модели
        сообщения текущего пользователя.
        """
        message = form.save()
        user = self.request.user
        message.author = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс отображения страницы редактирования сообщения.
    """
    model = Message
    form_class = MessageForm
    permission_required = 'newsletter.can_change_message'
    extra_context = {'title': 'Редактировать сообщение'}

    def get_success_url(self):
        """
        Переопределяем функцию для перенаправления
        на отредактированное сообщение.
        """
        return reverse("newsletter:message-detail", args=[self.kwargs.get("pk")])


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Класс отображения страницы детальной информации сообщения.
    """
    model = Message
    permission_required = 'newsletter.can_view_message'
    extra_context = {'title': 'Посмотреть сообщение'}


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс отображения страницы удаления сообщения.
    """
    model = Message
    success_url = reverse_lazy('newsletter:message-list')
    permission_required = 'newsletter.can_delete_message'
    extra_context = {'title': 'Удалить сообщение'}


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс отображения страницы списка сообщений.
    """
    model = Message
    permission_required = 'newsletter.can_view_message'
    extra_context = {'title': 'Список сообщений'}

    def get_queryset(self, *args, **kwargs):
        """
        Переопределяем функцию для проверки
        сообщения на принадлежность к текущему пользователю
        и на право просмотра.
        """
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.can_view_message'):
            return queryset
        queryset = queryset.filter(author=user)
        return queryset


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс отображения страницы создания клиента.
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client-list')
    permission_required = 'newsletter.can_add_client'
    extra_context = {'title': 'Добавить клиента'}

    def form_valid(self, form):
        """
        Переопределяем функцию для присваивания модели
        клиента текущего пользователя.
        """
        client = form.save()
        user = self.request.user
        client.author = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс отображения страницы редактирования клиента.
    """
    model = Client
    form_class = ClientForm
    permission_required = 'newsletter.can_change_client'
    extra_context = {'title': 'редактировать клиента'}

    def get_success_url(self):
        """
        Переопределяем функцию для перенаправления
        на отредактированного клиента.
        """
        return reverse("newsletter:client-detail", args=[self.kwargs.get("pk")])


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Класс отображения страницы детальной информации клиента.
    """
    model = Client
    permission_required = 'newsletter.can_view_client'
    extra_context = {'title': 'Просмотр клиента'}


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс отображения страницы удаления клиента.
    """
    model = Client
    success_url = reverse_lazy('newsletter:client-list')
    permission_required = 'newsletter.can_delete_client'
    extra_context = {'title': 'Удаление клиента'}


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс отображения страницы списка клиентов.
    """
    model = Client
    permission_required = 'newsletter.can_view_client'
    extra_context = {'title': 'Список клиентов'}

    def get_queryset(self, *args, **kwargs):
        """
        Переопределяем функцию для проверки
        клиента на принадлежность к текущему пользователю
        и на право просмотра.
        """
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.can_view_client'):
            return queryset
        queryset = queryset.filter(author=user)
        return queryset


class NewsLetterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс отображения страницы создания рассылки.
    """
    model = Newsletter
    form_class = CreateNewsletterForm
    success_url = reverse_lazy('newsletter:newsletter-list')
    permission_required = 'newsletter.can_add_newsletter'
    extra_context = {'title': 'Создать рассылку'}

    def form_valid(self, form):
        """
        Переопределяем функцию для присваивания
        модели рассылки текущего пользователя.
        """
        newsletter = form.save()
        user = self.request.user
        newsletter.author = user
        newsletter.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Переопределяем функцию для переопределения формы рассылки
        для проверки принадлежности связанных моделей рассылки
        к текущему пользователю.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class NewsletterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс отображения страницы редактирования рассылки.
    """
    model = Newsletter
    permission_required = 'newsletter.can_change_newsletter'
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        """
        Переопределяем функцию для перенаправления
        на отредактированную рассылку.
        """
        return reverse("newsletter:newsletter-detail", args=[self.kwargs.get("pk")])

    def get_form_kwargs(self):
        """
        Переопределяем функцию для переопределения формы рассылки
        для проверки принадлежности связанных моделей рассылки
        к текущему пользователю.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def get_form_class(self):
        """
        Переопределяем функцию дял передачи формы
        в соответствии с правами пользователя.
        """
        user = self.request.user
        if self.object.author == user:
            return UpdateNewsletterForm
        elif user.has_perm('newsletter.can_change_newsletter'):
            return UpdateModerNewsletterForm


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Класс отображения страницы детальной информации клиента.
    """
    model = Newsletter
    permission_required = 'newsletter.can_view_newsletter'
    extra_context = {'title': 'Просмотр рассылки'}

    def get_context_data(self, **kwargs):
        """
        Переопределяем функцию для отображения
        клиентов этой рассылки.
        """
        context = super().get_context_data(**kwargs)
        clients = list(self.object.clients.all())
        context['clients'] = ', '.join([str(client) for client in clients])
        return context


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс отображения страницы удаления рассылки.
    """
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter-list')
    permission_required = 'newsletter.can_delete_newsletter'
    extra_context = {'title': 'Удаление рассылки'}


class NewsletterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс отображения страницы списка рассылки.
    """
    model = Newsletter
    permission_required = 'newsletter.can_view_newsletter'
    extra_context = {'title': 'Список рассылок'}

    def get_queryset(self, *args, **kwargs):
        """
        Переопределяем функцию для проверки
        рассылки на принадлежность к текущему пользователю
        и на право просмотра.
        """
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.can_view_newsletter'):
            return queryset
        queryset = Newsletter.objects.filter(author=user)
        return queryset


def newsletter_history(request):
    """
    Функция отображения страницы попыток рассылки.
    """
    user = request.user
    history = HistoryNewsletter.objects.filter(newsletter__author=user)
    data = {
        'newsletter_history': history if user.has_perm('newsletter.can_view_newsletter') else None,
        'title': 'История рассылки'
    }
    return render(request, 'newsletter/newsletter_history.html', context=data)
