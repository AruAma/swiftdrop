from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    MessageViewSet, FileViewSet,
    register_view, login_view, logout_view,
    messages_view, files_view, profile_view,
    root_redirect, home_view,
)

# Роутер для API ViewSet'ов
router = DefaultRouter()
router.register('messages', MessageViewSet)
router.register('files', FileViewSet)

urlpatterns = [
    # Базовый редирект и главная
    path('', root_redirect),  # Например, редирект на login
    path('home/', home_view, name='home'),

    # Обычные веб-маршруты
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('messages/', messages_view, name='messages'),
    path('files/', files_view, name='files'),
    path('profile/', profile_view, name='profile'),

    # API маршруты
    path('api/', include(router.urls)),
    path('api/token-auth/', obtain_auth_token, name='token-auth'),
]
