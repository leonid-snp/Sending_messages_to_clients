from django.forms import ModelForm

from blog.models import Blog
from newsletter.form import StyleFormMixin


class BlogCreateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        exclude = ('views_count',)
