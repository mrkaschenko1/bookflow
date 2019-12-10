from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('search/', login_required(views.BookSearch.as_view()), name='book_search'),
    re_path(r'^search/add/(?P<id>.{1,20})/$', login_required(views.AddToBookshelf.as_view()), name='book_add'),
]