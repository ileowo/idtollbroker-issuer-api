from django.contrib import admin
from django.urls import path, include
from .views import get_certificates, request_certificates, check_certificate, get_certificate_schemas, get_certificate_schema_attributes, delete_certificate

urlpatterns = [
        path('/', get_certificates),
        path('/request', request_certificates),
        path('/check', check_certificate),
        path('/schema/attributes', get_certificate_schema_attributes),
        path('/schema', get_certificate_schemas),
        path('/delete', delete_certificate),
]
