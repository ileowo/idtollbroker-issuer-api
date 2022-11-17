from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from constance import config
import requests
import json

# Create your views here.
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def verify_certificate(request):
    organisation_id = config.PROCUREMENT_PORTAL_ORG_ID
    data_agreement_id = config.USER_VERIFICATION_DATA_AGREEMENT_ID
    connection_id = request.user.connection_id
    payload = { "connection_id": connection_id, "data_agreement_id": data_agreement_id }
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/present-proof/data-agreement-negotiation/offer"
    authorization_header = config.PROCUREMENT_PORTAL_API_KEY
    response = requests.post(url,json=payload, headers={"Authorization": authorization_header})
    if response.status_code == status.HTTP_200_OK:
        response = json.loads(response.text)
        presentation_exchange_id = response["presentation_exchange_id"]
        presentation_state = response["state"]
        presentation_record = response
        user = request.user
        user.presentation_exchange_id = presentation_exchange_id
        user.presentation_state = presentation_state
        user.presentation_record = presentation_record
        user.save()
        return JsonResponse(response)
    else:
        return Response(response.content, status=response.status_code)