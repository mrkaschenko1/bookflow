from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)


class Shelf(models.Model):
    name = models.CharField(max_length=150)
    books = models.ManyToManyField(Book, related_name='shelves', blank=True)