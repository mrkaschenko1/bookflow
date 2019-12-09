from django.contrib.auth.models import User
from django.db import models


class BookInfo(models.Model):
    google_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    authors = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    pageCount = models.IntegerField(blank=True, null=True)
    small_pic_url = models.URLField(max_length=1000, blank=True)


class Shelf(models.Model):
    name = models.CharField(max_length=150)
    books = models.ManyToManyField(BookInfo, related_name='shelves', blank=True)
    is_custom = models.BooleanField(default=True)
    profile = models.ForeignKey('accounts.Profile', related_name='shelves', blank=False, on_delete=models.CASCADE)
