from django.contrib import admin
from django.urls import path, include
from .views import get_connections, accept_invitation

urlpatterns = [
        path('/', get_connections),
        path('/accept_invitation', accept_invitation),
]
