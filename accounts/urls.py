from django.urls import path, include
from . import views

#app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/', views.update_profile, name='update_profile'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('avatar/change/', views.upload_pic, name='avatar_change'),
    # path('avatar/', include('avatar.urls'), name='change_avatar')
]