from django.contrib.auth.models import User
from django.db import models


class BookInfo(models.Model):
    google_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    authors = models.CharField(max_length=300, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    pageCount = models.IntegerField(blank=True, null=True)
    small_pic_url = models.URLField(max_length=1000, blank=True)

    def __str__(self):
        return self.title


class Shelf(models.Model):
    name = models.CharField(max_length=150)
    # books = models.ManyToManyField(BookInfo, related_name='shelves', blank=True)
    is_custom = models.BooleanField(default=True)
    profile = models.ForeignKey('accounts.Profile', related_name='shelves', blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user.username}: {self.name} shelf'


class Tag(models.Model):
    name = models.CharField(max_length=30)
    profile = models.ForeignKey('accounts.Profile', related_name='tags', blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProfileBookInfo(models.Model):
    profile = models.ForeignKey('accounts.Profile', related_name='profile_books', blank=False, null=False, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, related_name='profile_books', on_delete=models.CASCADE)
    book = models.ForeignKey(BookInfo, related_name='profile_books', blank=False, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField()
    tags = models.ManyToManyField(Tag, related_name='profile_books')

    def __str__(self):
        return f'{self.profile.user.username}: {self.book.title} book'