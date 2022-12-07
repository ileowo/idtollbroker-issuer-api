import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from constance import config

from certificate.models import Certificates

authorization = config.BYGG_AB_API_KEY


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_certificates(request):
    """
    certificates = Certificates.objects.filter(user=request.user).values('credential_exchange_id').all()
    return Response({
        'certificates': certificates,
    }, status=status.HTTP_200_OK)
    """
    organisation_id = config.BYGG_AB_ORG_ID
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/credentials?count=1000"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(response.json(), status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def request_certificates(request):
    certificate = request.GET.get("certificate")
    if certificate == "real_estate_insurance":
        organisation_id = config.FRIA_FORSAKRINGAR_ORG_ID
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
        api_key = config.FRIA_FORSAKRINGAR_API_KEY
        real_estate_insurance_cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG[
            'REAL_ESTATE_INSURANCE_CREDENTIAL_DEFINITION_ID']
        real_estate_insurance_connection_id = config.WALLET_USER_ISSUANCE_CONFIG[
            'REAL_ESTATE_INSURANCE_CONNECTION_ID']
        real_estate_insurance_data_agreement_id = config.WALLET_USER_ISSUANCE_CONFIG[
            'REAL_ESTATE_INSURANCE_DATA_AGREEMENT_ID']
        payload = {
            "comment": "Real estate insurance",
            "auto_remove": False,
            "trace": False,
            "cred_def_id": real_estate_insurance_cred_def_id,
            "connection_id": real_estate_insurance_connection_id,
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": [
                    {
                        "name": "Insurance number",
                        "value": "SR-234-01-F"
                    },
                    {
                        "name": "Org. number",
                        "value": "123400-7899"
                    },
                    {
                        "name": "Name",
                        "value": "Bygg AB"
                    },
                    {
                        "name": "Validity date",
                        "value": "2023-11-30"
                    }
                ]
            },
            "auto_issue": True,
            "data_agreement_id": real_estate_insurance_data_agreement_id
        }
    elif certificate == "ecolabel":
        organisation_id = config.ORNEN_ORG_ID
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
        api_key = config.ORNEN_API_KEY
        ecolabel_cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG[
            'ECOLABEL_CREDENTIAL_DEFINITION_ID']
        ecolabel_connection_id = config.WALLET_USER_ISSUANCE_CONFIG['ECOLABEL_CONNECTION_ID']
        ecolabel_data_agreement_id = config.WALLET_USER_ISSUANCE_CONFIG[
            'ECOLABEL_DATA_AGREEMENT_ID']
        payload = {
            "comment": "Ecolabel",
            "auto_remove": False,
            "trace": False,
            "cred_def_id": ecolabel_cred_def_id,
            "connection_id": ecolabel_connection_id,
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": [
                    {
                        "name": "License number",
                        "value": "3019 2143"
                    }
                ]
            },
            "auto_issue": True,
            "data_agreement_id": ecolabel_data_agreement_id
        }
    else:
        organisation_id = config.BOLAGSVERKET_ORG_ID
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
        api_key = config.BYGG_AB_API_KEY
        cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG['CREDENTIAL_DEFINITION_ID']
        connection_id = config.WALLET_USER_ISSUANCE_CONFIG['CONNECTION_ID']
        data_agreement_id = config.WALLET_USER_ISSUANCE_CONFIG['DATA_AGREEMENT_ID']
        payload = {
            "comment": "Certificate of registration and register extract",
            "auto_remove": False,
            "trace": False,
            "cred_def_id": cred_def_id,
            "connection_id": connection_id,
            "data_agreement_id": data_agreement_id,
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": [
                    {"name": "name", "value": "Bygg AB"},
                    {"name": "legalForm", "value": "Aktiebolag"},
                    {"name": "activity", "value": "Construction Industry"},
                    {"name": "registrationDate", "value": "2005-10-08"},
                    {"name": "legalStatus", "value": "ACTIVE"},
                    {
                        "name": "registeredAddress.fullAddress",
                        "value": "Sveavägen 48, 111 34 Stockholm, Sweden",
                    },
                    {"name": "registeredAddress.thoroughFare", "value": "Sveavägen"},
                    {"name": "registeredAddress.locatorDesignator", "value": "48"},
                    {"name": "registeredAddress.postCode", "value": "111 34"},
                    {"name": "registeredAddress.postName", "value": "Stockholm"},
                    {"name": "registeredAddress.adminUnitLevel1", "value": "SE"},
                ],
            },
            "auto_issue": True,
        }

    response = requests.post(
        url,
        headers={
            "Authorization": api_key,
            "content-type": "application/json;charset=UTF-8",
        },
        json=payload,
    )
    if response.status_code == 200:
        instance = Certificates.objects.create(
            user=request.user,
            credential_exchange_id=response.json().get("credential_exchange_id"),
        )
        instance.save()
        return Response(response.json(), status=response.status_code)
    else:
        return Response(response.text, status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def check_certificate(request):
    credential_exchange_id = request.GET["credential_exchange_id"]
    url = f"https://cloudagent.igrant.io/v1/624c025d7eff6f000164bb94/admin/issue-credential/records/{credential_exchange_id}"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(response.json(), status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_certificate_schemas(request):
    organisation_id = request.GET["organisation_id"]
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/v1/data-agreements?method_of_use=data-source&publish_flag=true&page=1&page_size=1000000"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(response.json(), status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_certificate_schema_attributes(request):
    organisation_id = request.GET["organisation_id"]
    schema_id = request.GET["schema_id"]
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/schemas/{schema_id}"
    print(url)
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(response.json(), status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["DELETE"])
def delete_certificate(request):
    organisation_id = request.GET["organisation_id"]
    referent = request.GET["referent"]
    url = (
        f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/credential/{referent}"
    )
    response = requests.delete(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    return Response(status=response.status_code)
