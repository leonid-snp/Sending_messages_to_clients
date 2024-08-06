import random

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from blog.models import Blog
from newsletter.form import (ClientForm, CreateNewsletterForm, MessageForm,
                             UpdateModerNewsletterForm, UpdateNewsletterForm)
from newsletter.models import Client, HistoryNewsletter, Message, Newsletter


class HomeTemplateView(TemplateView):
    template_name = 'newsletter/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        blog = list(Blog.objects.all())
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
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message-list')
    permission_required = 'newsletter.add_message'
    extra_context = {'title': 'Создать сообщение'}

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.author = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'newsletter.change_message'
    extra_context = {'title': 'Редактировать сообщение'}

    def get_success_url(self):
        return reverse("newsletter:message-detail", args=[self.kwargs.get("pk")])


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    permission_required = 'newsletter.view_message'
    extra_context = {'title': 'Посмотреть сообщение'}


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message-list')
    permission_required = 'newsletter.delete_message'
    extra_context = {'title': 'Удалить сообщение'}


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    permission_required = 'newsletter.view_message'
    extra_context = {'title': 'Список сообщений'}

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.view_message'):
            return queryset
        queryset = queryset.filter(author=user)
        return queryset


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client-list')
    permission_required = 'newsletter.add_client'
    extra_context = {'title': 'Добавить клиента'}

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.author = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'newsletter.change_client'
    extra_context = {'title': 'редактировать клиента'}

    def get_success_url(self):
        return reverse("newsletter:client-detail", args=[self.kwargs.get("pk")])


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'newsletter.view_client'
    extra_context = {'title': 'Просмотр клиента'}


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client-list')
    permission_required = 'newsletter.delete_client'
    extra_context = {'title': 'Удаление клиента'}


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = 'newsletter.view_client'
    extra_context = {'title': 'Список клиентов'}

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.view_client'):
            return queryset
        queryset = queryset.filter(author=user)
        return queryset


class NewsLetterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Newsletter
    form_class = CreateNewsletterForm
    success_url = reverse_lazy('newsletter:newsletter-list')
    permission_required = 'newsletter.add_newsletter'
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


class NewsletterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newsletter
    permission_required = 'newsletter.change_newsletter'
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse("newsletter:newsletter-detail", args=[self.kwargs.get("pk")])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if self.object.author == user:
            return UpdateNewsletterForm
        elif user.has_perm('newsletter.change_newsletter'):
            return UpdateModerNewsletterForm


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Newsletter
    permission_required = 'newsletter.view_newsletter'
    extra_context = {'title': 'Просмотр рассылки'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = list(self.object.clients.all())
        context['clients'] = ', '.join([str(client) for client in clients])
        return context


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter-list')
    permission_required = 'newsletter.delete_newsletter'
    extra_context = {'title': 'Удаление рассылки'}


class NewsletterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Newsletter
    permission_required = 'newsletter.view_newsletter'
    extra_context = {'title': 'Список рассылок'}

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if user.has_perm('newsletter.view_newsletter'):
            return queryset
        queryset = Newsletter.objects.filter(author=user)
        return queryset


def newsletter_history(request):
    user = request.user
    print(request.__dict__)
    history = HistoryNewsletter.objects.filter(newsletter__author=user)
    data = {
        'newsletter_history': history,
        'title': 'История рассылки'
    }
    return render(request, 'newsletter/newsletter_history.html', context=data)
