from django.contrib import admin
from django.urls import path, include
from .views import get_certificates, request_certificates, check_certificate

urlpatterns = [
        path('/', get_certificates),
        path('/request', request_certificates),
        path('/check', check_certificate)
]
