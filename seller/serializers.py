from rest_framework import serializers
from .models import Responses


class ResponsesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    presentation_exchange_id = serializers.CharField(max_length=250)
    presentation_state  = serializers.CharField(max_length=250)
    presentation_record = serializers.JSONField()
