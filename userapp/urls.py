from django.urls import path
from . import views
from .views import (
    UserProfileAPIView, NotificationListAPIView,
    TokenObtainPairViewWithUserData, TokenRefreshViewWithUserData, TokenRefreshAPIView
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_user_role/<int:user_id>/', views.edit_user_role, name='edit_user_role'),
    path('request_author_status/', views.request_author_status, name='request_author_status'),
    path('notifications/', views.notifications, name='notifications'),
    path('api/profile/', UserProfileAPIView.as_view(), name='profile-api'),
    path('api/notifications/', NotificationListAPIView.as_view(), name='notifications-api'),
    path('api/token/', TokenObtainPairViewWithUserData.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewWithUserData.as_view(), name='token_refresh'),
    path('api/token/refresh/custom/', TokenRefreshAPIView.as_view(), name='token_refresh_custom'),
]