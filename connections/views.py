from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from pob_backend.settings import COMPANY_AGENT_URL, ISSUER_AGENT_URL
from igrant_user.models import IGrantUser
from rest_framework.response import Response
from rest_framework import status
from connections.models import Invitations
from django.views.decorators.csrf import csrf_exempt
import json
import base64

import requests


@csrf_exempt
@api_view(["GET"])
def get_default_wallet(request):
    organisation_id = "624c025d7eff6f000164bb94"
    authorization = "ApiKey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI2MzQzZWM0ZjZkZTVkNzAwMDFhYzAzOGQiLCJvcmdpZCI6IiIsImVudiI6IiIsImV4cCI6MTY5NjUwMDAxOH0.8hSeQhWhU0xg8mbJbqNhx8OHHDF_PkJdNiRrAvgkjEs"
    url = f"https://staging-api.igrant.io/v1/organizations/{organisation_id}/aries-cloudagent"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(response.json(), status=response.status_code)


def get_endpoint(request):
    endpoint = ""
    if request.user.user_type == IGrantUser.UserType.COMPANY:
        endpoint = COMPANY_AGENT_URL
    else:
        endpoint = ISSUER_AGENT_URL
    print(endpoint)
    return endpoint


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_connections(request):
    url = "https://staging-api.igrant.io/v1/organizations/624c025d7eff6f000164bb94/aries-cloudagent"
    authorization_header = "ApiKey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI2MzQzZWM0ZjZkZTVkNzAwMDFhYzAzOGQiLCJvcmdpZCI6IiIsImVudiI6IiIsImV4cCI6MTY5NjUwMDAxOH0.8hSeQhWhU0xg8mbJbqNhx8OHHDF_PkJdNiRrAvgkjEs"
    response = requests.get(url, headers={"Authorization": authorization_header})
    return Response(response.json(), status=response.status_code)

    return
    """
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
    """


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def accept_invitation(request):
    endpoint = get_endpoint(request)
    body = request.data
    print(body)
    connection_url = body.get("connection_url", None)
    if connection_url is not None:
        payload = {"connection_url": connection_url}
        response = requests.post(
            endpoint + "/v2/connections/receive-invitation?auto_accept=true",
            json=payload,
        )
        if response.status_code == status.HTTP_200_OK:
            connection = response.json()
            connection_id = connection.get("connection_id")
            connection_data = connection_url.split("c_i=")[-1]
            connection_data = str(base64.b64decode(connection_data))

            invitation, created = Invitations.objects.get_or_create(
                user=request.user, connection_id=connection_id
            )
            invitation.invitation_data = connection_data
            invitation.save()
            return Response(response.json(), status=response.status_code)
        else:
            return Response(response.content, status=response.status_code)
    else:
        return Response(" connection_url required", status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def receive_invitation(request):
    organisation_id = "6364ee3781f7df00012cdaba"
    body = request.data
    connection_url = body.get("connection_url", None)
    if connection_url is not None:
        connection_data = connection_url.split("c_i=")[-1]
        connection_data = base64.b64decode(connection_data)
        connection_data = json.loads(connection_data)
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/connections/receive-invitation?auto_accept=true"
        authorization_header = "ApiKey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI2MzY0ZWUwNjgxZjdkZjAwMDEyY2RhYjkiLCJvcmdpZCI6IiIsImVudiI6IiIsImV4cCI6MTY5ODY2MzI5N30.XAgBDTmlJwofuCF_P-rLoVxTBeJuKQYKtYhiyji1kS0"
        response = requests.post(url,json=connection_data, headers={"Authorization": authorization_header})
        response = json.loads(response.text)
        connection_id = response["connection_id"]
        connection_state = response["state"]
        user = request.user
        user.connection_id = connection_id
        user.connection_state = connection_state
        user.save()
        return Response(response)
    else:
        return Response(" connection_url required", status=status.HTTP_400_BAD_REQUEST)
