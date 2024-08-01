from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from newsletter.form import MessageForm, ClientForm, CreateNewsletterForm, UpdateNewsletterForm
from newsletter.models import Client, Message, Newsletter


class HomeTemplateView(TemplateView):
    template_name = 'newsletter/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        newsletter = Newsletter.objects.all()
        clients = Client.objects.all()
        count = 0
        unique_client = []
        activ = []
        for item in newsletter:
            count += 1
            unique_client.append(item.clients)
            if item.status == 'запущена':
                activ.append(item)

        data = {
            'count_newsletter': count,
            'activ_newsletter': activ
        }
        return super().get_context_data(**data)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message-list')
    extra_context = {'title': 'Создать сообщение'}

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.author = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Редактировать сообщение'}

    def get_success_url(self):
        return reverse("newsletter:message-detail", args=[self.kwargs.get("pk")])


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Посмотреть сообщение'}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message-list')
    extra_context = {'title': 'Удалить сообщение'}


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {'title': 'Список сообщений'}

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(author=user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client-list')
    extra_context = {'title': 'Добавить клиента'}

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.author = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'редактировать клиента'}

    def get_success_url(self):
        return reverse("newsletter:client-detail", args=[self.kwargs.get("pk")])


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {'title': 'Просмотр клиента'}


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client-list')
    extra_context = {'title': 'Удаление клиента'}


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {'title': 'Список клиентов'}

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(author=user)
        return queryset


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = CreateNewsletterForm
    success_url = reverse_lazy('newsletter:newsletter-list')
    extra_context = {'title': 'Создать рассылку'}

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.author = user
        newsletter.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = UpdateNewsletterForm
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse("newsletter:newsletter-detail", args=[self.kwargs.get("pk")])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    extra_context = {'title': 'Просмотр рассылки'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = list(self.object.clients.all())
        context['clients'] = ', '.join([str(client) for client in clients])
        return context


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter-list')
    extra_context = {'title': 'Удаление рассылки'}


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    extra_context = {'title': 'Список рассылок'}

    def get_queryset(self):
        user = self.request.user
        self.queryset = Newsletter.objects.filter(author=user)
        return self.queryset.all()
