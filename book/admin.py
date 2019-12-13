from django.contrib import admin
from .models import BookInfo, Shelf, ProfileBookInfo

# Register your models here.

admin.site.register(BookInfo)
admin.site.register(Shelf)
admin.site.register(ProfileBookInfo)
