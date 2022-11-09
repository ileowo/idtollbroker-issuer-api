from .models import IGrantUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class IGrantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGrantUser
        fields = ['id', 'email', 'fullname', 'user_type', 'org', 'connection_id', 'connection_state', 'presentation_exchange_id', 'presentation_state', 'presentation_record']


class CustomTokenSerializer(serializers.ModelSerializer):
    user = IGrantUserSerializer(many=False, read_only=True)


    class Meta:
        model = Token
        fields = ('key', 'user')