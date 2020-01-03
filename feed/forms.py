from django import forms
from django.contrib.auth.models import User

from .models import Post


class PostForm(forms.ModelForm):
    # books = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__icontains='maintainer')

    class Meta:
        model = Post
        fields = ('title', 'body', 'books')