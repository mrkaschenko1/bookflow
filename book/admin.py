from django.contrib import admin

from bookflow import settings
from .models import BookInfo, Shelf, ProfileBookInfo, Tag

# Register your models here.

if settings.DEBUG:
    admin.site.register(BookInfo)
# admin.site.register(BookInfo)
# admin.site.register(Shelf)
# admin.site.register(ProfileBookInfo)
# admin.site.register(Tag)
