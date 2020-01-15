from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('profile/wall/create/', views.CreateCrudPost.as_view(), name='crud_ajax_create_post'),
    path('profile/wall/update/', views.UpdateCrudPost.as_view(), name='crud_ajax_update_post'),
    path('profile/wall/delete/', views.DeleteCrudPost.as_view(), name='crud_ajax_delete_post'),
    path('wall/', views.PostList.as_view(), name='feed'),
    path('wall/like', views.PostLikeToggle.as_view(), name='like_toggle')
]