from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from blog.forms import BlogCreateForm
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')


class BlogDetailView(DetailView):
    model = Blog


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


class BlogListView(ListView):
    model = Blog
