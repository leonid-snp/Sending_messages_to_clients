from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import BlogCreateForm
from blog.models import Blog


class BlogCreateView(CreateView):
    """
    Модель создания статьи блога.
    """
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Создание статьи'}


class BlogUpdateView(UpdateView):
    """
    Модель редактирования статьи блога.
    """
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Редактирование статьи'}


class BlogDetailView(DetailView):
    """
    Модель детального просмотра статьи блога.
    """
    model = Blog
    extra_context = {'title': 'Просмотр статьи'}


class BlogDeleteView(DeleteView):
    """
    Модуль удаления статьи блога.
    """
    model = Blog
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Удаление статьи'}


class BlogListView(ListView):
    """
    Модель вывода всех статей блога.
    """
    model = Blog
    extra_context = {'title': 'Список статей'}
