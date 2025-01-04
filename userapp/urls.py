from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_user_role/<int:user_id>/', views.edit_user_role, name='edit_user_role'),
    path('request_author_status/', views.request_author_status, name='request_author_status'),
    path('notifications/', views.notifications, name='notifications'),
]