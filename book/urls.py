from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', login_required(views.show_books), name='book_list'),
    path('delete/', login_required(views.delete_book), name='delete_book'),
    path('search/', login_required(views.BookSearch.as_view()), name='book_search'),
    re_path(r'^search/add/(?P<id>.{1,20})/$', login_required(views.AddToBookshelf.as_view()), name='book_add'),
]