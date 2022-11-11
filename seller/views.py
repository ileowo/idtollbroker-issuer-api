from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from buyer.serializers import TenderSerializer,RequirementSerializer
from igrant_user.models import IGrantUser
from buyer.models import Tender, Requirement
from .models import Responses
from django.http import JsonResponse
from rest_framework.response import Response
import requests
import json

# Create your views here.
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_tender(request, tender_id):
    user = request.user
    tender = get_object_or_404(Tender, pk=tender_id)
    tender_name = tender.name
    buyer_id = tender.user.id
    buyer = get_object_or_404(IGrantUser, pk=buyer_id)
    buyer_name = buyer.org
    buyer_address = buyer.address
    buyer_country = buyer.country
    buyer_presentation_record = buyer.presentation_record
    requirements = Requirement.objects.filter(tender_id=tender.id)
    serializer = RequirementSerializer(requirements, many=True)
    requirement_data = serializer.data
    for requirement in requirement_data:
        response = Responses.objects.get(tender=tender.id,requirements=requirement["id"])
        if response.presentation_state == "verified":
            requirement["submission_status"] = True
        else:
            requirement["submission_status"] = False
    responses = {
        "name": tender_name,
        "buyer":
        {
            "name": buyer_name, "address": buyer_address, "country": buyer_country, "presentation_record": buyer_presentation_record
        },
        "requirement": requirement_data
    }
    return JsonResponse(responses)
    

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"]) 
def verify_certificate(request,tender_id,requirement_id):
    organisation_id = "6364ee3781f7df00012cdaba"
    body = request.data
    data_agreement_id = body.get("data_agreement_id", None)
    user = request.user
    connection_id = user.connection_id
    payload = { "connection_id": connection_id, "data_agreement_id": data_agreement_id }
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/present-proof/data-agreement-negotiation/offer"
    authorization_header = "ApiKey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI2MzY0ZWUwNjgxZjdkZjAwMDEyY2RhYjkiLCJvcmdpZCI6IiIsImVudiI6IiIsImV4cCI6MTY5ODY2MzI5N30.XAgBDTmlJwofuCF_P-rLoVxTBeJuKQYKtYhiyji1kS0"
    response = requests.post(url,json=payload, headers={"Authorization": authorization_header})
    if response.status_code == status.HTTP_200_OK:
        response = json.loads(response.text)
        presentation_exchange_id = response["presentation_exchange_id"]
        presentation_state = response["state"]
        presentation_record = response
        tender = get_object_or_404(Tender, pk=tender_id)
        requirement = get_object_or_404(Requirement, pk=requirement_id)
        supplier = get_object_or_404(IGrantUser, pk=user.id)
        responses = Responses.objects.get_or_create(tender=tender,requirements=requirement,supplier=supplier)
        responses.presentation_exchange_id = presentation_exchange_id
        responses.presentation_state = presentation_state
        responses.presentation_record = presentation_record
        responses.save()
        return JsonResponse(response)
    else:
        return Response(response.content, status=response.status_code)