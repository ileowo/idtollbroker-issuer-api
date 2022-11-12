from .models import IGrantUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class IGrantUserSerializer(serializers.ModelSerializer):
    org = serializers.CharField(source='get_org_display')

    class Meta:
        model = IGrantUser
        fields = ['id', 'email', 'fullname', 'address', 'country', 'user_type', 'org', 'org_verification_status', 'connection_id', 'connection_state', 'presentation_exchange_id', 'presentation_state', 'presentation_record']


class CustomTokenSerializer(serializers.ModelSerializer):
    user = IGrantUserSerializer(many=False, read_only=True)


    class Meta:
        model = Token
        fields = ('key', 'user')


class IGrantUsersSerializer(serializers.ModelSerializer):
    org = serializers.CharField(source='get_org_display')
    org_verification_status = serializers.CharField(source='get_org_verification_status_display')

    class Meta:
        model = IGrantUser
        fields = ['id', 'email', 'fullname', 'address', 'country', 'user_type', 'org', 'org_verification_status', 'presentation_record']