from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.BookSearch.as_view(), name='book_search'),
]