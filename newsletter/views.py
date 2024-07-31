from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from newsletter.form import MessageForm, ClientForm, NewsletterForm
from newsletter.models import Client, Message, Newsletter


class HomeTemplateView(TemplateView):
    template_name = 'newsletter/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        newsletter = Newsletter.objects.all()
        count = 0
        activ = []
        for item in newsletter:
            count += 1
            if item.status == 'запущена':
                activ.append(item)

        data = {
            'count_newsletter': count,
            'activ_newsletter': activ
        }
        return super().get_context_data(**data)


class MessageCreateView(CreateView):
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


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Редактировать сообщение'}

    def get_success_url(self):
        return reverse("newsletter:message-detail", args=[self.kwargs.get("pk")])


class MessageDetailView(DetailView):
    model = Message
    extra_context = {'title': 'Посмотреть сообщение'}


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message-list')
    extra_context = {'title': 'Удалить сообщение'}


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Список сообщений'}


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client-list')
    extra_context = {'title': 'Добавить клиента'}


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'редактировать клиента'}

    def get_success_url(self):
        return reverse("newsletter:client-detail", args=[self.kwargs.get("pk")])


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Просмотр клиента'}


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client-list')
    extra_context = {'title': 'Удаление клиента'}


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Список клиентов'}


class NewsLetterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter-list')
    extra_context = {'title': 'Создать рассылку'}

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.author = user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse("newsletter:newsletter-detail", args=[self.kwargs.get("pk")])


class NewsletterDetailView(DetailView):
    model = Newsletter
    extra_context = {'title': 'Просмотр рассылки'}

    def get_context_data(self, **kwargs):
        user = self.request.user
        list_newsletter = Newsletter.objects.all()

        clients_newsletter = []
        for newsletter in list_newsletter:
            clients_newsletter.append(Client.objects.filter(newsletter__id=newsletter.id))

        data = {
            'clients': clients_newsletter
        }
        return super().get_context_data(**data)


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter-list')
    extra_context = {'title': 'Удаление рассылки'}


class NewsletterListView(ListView):
    model = Newsletter
    extra_context = {'title': 'Список рассылок'}
