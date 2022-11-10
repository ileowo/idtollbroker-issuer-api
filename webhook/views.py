from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from igrant_user.models import IGrantUser
from seller.models import Responses
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
@require_POST
def receive_invitation(request):
    
    response = request.body
    response = json.loads(response)
    connection_id = response["connection_id"]
    connection_state = response["state"]
    user = get_object_or_404(IGrantUser,connection_id = connection_id)
    if user.connection_state == "active":
        return HttpResponse(status=status.HTTP_200_OK)
    else:
        user.connection_state = connection_state
        user.save()
        return HttpResponse(status=status.HTTP_200_OK)


@csrf_exempt
@require_POST
def verify_certificate(request):
    response = request.body
    response = json.loads(response)
    presentation_exchange_id = response["presentation_exchange_id"]
    presentation_state = response["state"]
    presentation_record = response
    user = IGrantUser.objects.get(presentation_exchange_id = presentation_exchange_id)
    if not user:
        response = Responses.objects.get(presentation_exchange_id = presentation_exchange_id)
        if response.presentation_state == "verified":
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            response.presentation_state = presentation_state
            response.presentation_record = presentation_record
            response.save()
            return HttpResponse(status=status.HTTP_200_OK)
    else:
        if user.presentation_state == "verified":
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            user.presentation_state = presentation_state
            user.presentation_record = presentation_record
            user.save()
            if presentation_state == "verified":
                user.org_verification_status = "VERIFIED"
                user.save()
            return HttpResponse(status=status.HTTP_200_OK)
