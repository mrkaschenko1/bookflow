from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('profile/wall/', login_required(views.PostCrudView.as_view()), name='show_posts'),
    path('profile/wall/create/', views.CreateCrudPost.as_view(), name='crud_ajax_create_post'),
    path('profile/wall/update/', views.UpdateCrudPost.as_view(), name='crud_ajax_update_post'),
    path('profile/wall/delete/', views.DeleteCrudPost.as_view(), name='crud_ajax_delete_post'),

    # path('', login_required(views.show_books), name='book_list'),
    # path('tag/<str:tag_name>', login_required(views.show_books_by_tag), name='book_list_by_tag'),
    # path('delete/', login_required(views.delete_book), name='delete_book'),
    # path('move/', login_required(views.move_book), name='move_book'),
    # path('search/', login_required(views.BookSearch.as_view()), name='book_search'),
    # re_path(r'^search/add/(?P<id>.{1,20})/$', login_required(views.AddToBookshelf.as_view()), name='book_add'),
    # path('add/tags/', login_required(AddTagToBookAjax.as_view()), name='add_tag_to_book'),
    # path('delete/tag/', login_required(DeleteTagFromBookAjax.as_view()), name='delete_tag_from_book'),
]