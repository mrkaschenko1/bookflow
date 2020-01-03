from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField(max_length=2000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
