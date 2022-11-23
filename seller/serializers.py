from rest_framework import serializers
from igrant_user.serializers import IGrantUsersSerializer
from .models import Responses


class ResponsesSerializer(serializers.Serializer):
    supplier = IGrantUsersSerializer(read_only=True)
    id = serializers.IntegerField()
    presentation_exchange_id = serializers.CharField(max_length=250)
    presentation_state  = serializers.CharField(max_length=250)
    presentation_record = serializers.JSONField()


class ResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Responses
        fields = ['id', 'requirements', 'presentation_exchange_id', 'presentation_state', 'presentation_record',]