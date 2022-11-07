from .models import IGrantUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class IGrantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGrantUser
        fields = ['id', 'email', 'user_type', 'org']


class CustomTokenSerializer(serializers.ModelSerializer):
    user = IGrantUserSerializer(many=False, read_only=True)


    class Meta:
        model = Token
        fields = ('key', 'user')