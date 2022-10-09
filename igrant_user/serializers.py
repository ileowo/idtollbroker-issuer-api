from .models import IGrantUser
from rest_framework import serializers


class IGrantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGrantUser
        fields = ['id', 'email', 'user_type']
