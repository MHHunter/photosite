from django.urls import path
from . import views
from .views import delete_photo

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('public/', views.public_photos, name='public_photos'),
    path('like/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('search/', views.search_users, name='search_users'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('photo/delete/<int:photo_id>/', delete_photo, name='delete_photo'),
]