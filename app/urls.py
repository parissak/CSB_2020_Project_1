from django.urls import path
from .views import homePageView, messageView, registerView, userPage

urlpatterns = [
    path('', homePageView, name='home'),
    path('users/<str:username>/messages', messageView, name='messages'),
    path('register/', registerView, name='register'),
    path('users/<str:username>', userPage, name='userpage'),
]