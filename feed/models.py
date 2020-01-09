from django.db import models
from django.contrib.auth.models import User

from book.models import BookInfo


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField(max_length=2000, blank=False, null=False)
    books = models.ManyToManyField(BookInfo, related_name='posts', null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_liked')
    created_at = models.DateTimeField(auto_now_add=True)
