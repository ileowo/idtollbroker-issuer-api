from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from igrant_user.models import IGrantUser
from rest_framework import status
import json

# Create your views here.
@require_POST
def receive_invitation(request):
    response = request.body
    response = json.loads(response)
    connection_id = response["connection_id"]
    connection_state = response["state"]
    user = get_object_or_404(IGrantUser,connection_id = connection_id)
    user.connection_state = connection_state
    user.save()
    return HttpResponse(status=status.HTTP_200_OK)
