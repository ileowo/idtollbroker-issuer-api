from django.urls import path

from . import views

urlpatterns = [
    path('tender/<int:tender_id>/', views.get_tender),
    path('tender/<int:tender_id>/requirement/<int:requirement_id>/verify-certificate', views.verify_certificate),
]