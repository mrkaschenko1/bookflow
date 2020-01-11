from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views


#app_name = "accounts"
def login_forbidden(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous, login_url='/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


urlpatterns = [
    path('password_reset/', login_forbidden(auth_views.PasswordResetView.as_view()), name='password_reset'),
    path('password_reset/done/', login_forbidden(auth_views.PasswordResetDoneView.as_view()), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', login_forbidden(auth_views.PasswordResetConfirmView.as_view()), name='password_reset_confirm'),
    path('reset/done/', login_forbidden(auth_views.PasswordResetCompleteView.as_view()), name='password_reset_complete'),
    path('login/', login_forbidden(auth_views.LoginView.as_view()), name='login'),
    path('signup/', login_forbidden(views.SignUp.as_view()), name='signup'),
    path('update/', views.update_profile, name='profile_update'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('avatar/delete/', views.delete_pic, name='avatar_delete'),
    path('tags/manage/', views.TagCrudView.as_view(), name='tags_manage'),
    path('tags/manage/create/', views.CreateCrudTag.as_view(), name='crud_ajax_create_tag'),
    path('tags/manage/update/', views.UpdateCrudTag.as_view(), name='crud_ajax_update_tag'),
    path('tags/manage/delete/', views.DeleteCrudTag.as_view(), name='crud_ajax_delete_tag'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile_info'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
    # path('avatar/', include('avatar.urls'), name='change_avatar')
]
