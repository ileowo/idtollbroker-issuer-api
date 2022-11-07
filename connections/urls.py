from django.contrib import admin
from django.urls import path, include
from .views import get_connections, accept_invitation, get_default_wallet, receive_invitation

urlpatterns = [
        path('/', get_connections),
        path('/default', get_default_wallet),
        path('/accept_invitation', accept_invitation),
        path('/receive-invitation', receive_invitation),
]
