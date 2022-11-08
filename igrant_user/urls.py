from django.contrib import admin
from django.urls import path, include
from .views import UserList, UserDetail, AdminResetConnection

urlpatterns = [
        path('/', UserList.as_view()),
        path('/<int:pk>/', UserDetail.as_view()),
        path('/admin/reset-connection', AdminResetConnection),
]
