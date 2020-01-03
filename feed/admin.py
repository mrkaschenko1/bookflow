from django.contrib import admin

# Register your models here.
from feed.models import Post

admin.site.register(Post)
