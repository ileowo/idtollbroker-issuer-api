from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from pop_backend.settings import COMPANY_AGENT_URL, ISSUER_AGENT_URL
from igrant_user.models import IGrantUser
from rest_framework.response import Response
from rest_framework import status
from .models import Invitations
import json
import base64

import requests

def get_endpoint(request):
    endpoint = ''
    if request.user.user_type == IGrantUser.UserType.COMPANY:
        endpoint = COMPANY_AGENT_URL
    else:
        endpoint = ISSUER_AGENT_URL
    print(endpoint)
    return endpoint

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def get_connections(request):
    endpoint = get_endpoint(request)
    response = requests.get(endpoint + '/connections')
    results = response.json().get('results', None)
    if results is not None:
        ids = [x['connection_id'] for x in results]
        invitation_data = Invitations.objects.filter(connection_id__in=ids).values_list(
                            'connection_id', 'invitation_data')
    return Response({
        'result': results,
        'invitation_data': invitation_data
    }, status=response.status_code)

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def accept_invitation(request):
    endpoint = get_endpoint(request)
    body = request.data
    print(body)
    connection_url = body.get('connection_url', None)
    if connection_url is not None:
        payload = {
            "connection_url": connection_url
        }
        response = requests.post(endpoint + '/v2/connections/receive-invitation?auto_accept=true', json=payload)
        if response.status_code == status.HTTP_200_OK:
            connection = response.json()
            connection_id = connection.get('connection_id')
            connection_data = connection_url.split('c_i=')[-1]
            connection_data = str(base64.b64decode(connection_data))

            invitation, created = Invitations.objects.get_or_create(user=request.user, connection_id=connection_id)
            invitation.invitation_data = connection_data
            invitation.save()
            return Response(response.json(), status=response.status_code)
        else:
            return Response(response.content, status=response.status_code)
    else:
        return Response(" connection_url required", status=status.HTTP_400_BAD_REQUEST)
