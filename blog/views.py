from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from blog.forms import BlogCreateForm
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Создание статьи'}


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Редактирование статьи'}


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'Просмотр статьи'}


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Удаление статьи'}


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': 'Список статей'}
