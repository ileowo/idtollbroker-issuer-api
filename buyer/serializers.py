from rest_framework import serializers
from .models import Requirement, Tender


class TenderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=16)


class RequirementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    issuer = serializers.CharField(max_length=250)
    issuer_logo_url = serializers.CharField(max_length=512)
    data_agreement_id = serializers.CharField(max_length=250)
    category = serializers.CharField(max_length=256)
    requirement_header = serializers.CharField(max_length=256)
    requirement_description = serializers.CharField(max_length=256)
    requirement_category = serializers.CharField(max_length=256)