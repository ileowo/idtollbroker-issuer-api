from django.urls import path

from . import views

urlpatterns = [
    path('topic/connections/',views.receive_invitation),
]