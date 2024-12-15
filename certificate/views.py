import requests
import base64
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from constance import config
from typing import Tuple

from certificate.models import Certificates, OpenID4VCCertificate


def decode_header_and_claims_in_jwt(token: str) -> Tuple[dict, dict]:
    headers_encoded, claims_encoded, _ = token.split(".")
    claims_decoded = base64.b64decode(
        claims_encoded + "=" * (-len(claims_encoded) % 4)
    )
    headers_decoded = base64.b64decode(
        headers_encoded + "=" * (-len(headers_encoded) % 4)
    )
    return (json.loads(headers_decoded), json.loads(claims_decoded))


def decode_disclosure(disclosure: str):
    disclosure_decoded = base64.b64decode(
        disclosure + "=" * (-len(disclosure) % 4)
    )
    return json.loads(disclosure_decoded)


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
    authorization = config.BYGG_AB_API_KEY
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/credentials?count=1000"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )

    # Iterate through pending certificates and try to resolve the credential
    pending_oid4vc_certificates = OpenID4VCCertificate.objects.filter(
        status="pending"
    )
    for pending_oid4vc_certificate in pending_oid4vc_certificates:
        authorization_header = config.BYGG_AB_OPENID4VC_API_KEY
        headers = {"Authorization": authorization_header}
        credential_response = requests.put(
            f"https://demo-api.igrant.io/v2/config/digital-wallet/openid/sdjwt/credential/{pending_oid4vc_certificate.acceptance_token}/receive-deferred",
            json={},
            headers=headers,
        )
        if credential_response.status_code == 200:
            credential_response_json = credential_response.json()
            if (
                credential_response_json.get("credential", {}).get(
                    "credentialStatus", ""
                )
                == "credential_acked"
            ):
                legalName = (
                    credential_response_json.get("credential", {})
                    .get("credential", {})
                    .get("legalName", "")
                )
                identifier = (
                    credential_response_json.get("credential", {})
                    .get("credential", {})
                    .get("identifier", "")
                )
                credential = {"legalName": legalName, "identifier": identifier}
                pending_oid4vc_certificate.credential = credential
                pending_oid4vc_certificate.status = "ready"
                pending_oid4vc_certificate.credentialJwt = (
                    credential_response_json.get("credential", "")
                )
                pending_oid4vc_certificate.save()

    certificate_response = response.json()
    if isinstance(certificate_response.get("results"), list):
        ready_oid4vc_certificates = OpenID4VCCertificate.objects.filter(
            status="ready"
        )
        for ready_oid4vc_certificate in ready_oid4vc_certificates:
            certificate_response.get("results").append(
                {
                    "referent": ready_oid4vc_certificate.acceptance_token,
                    "attrs": ready_oid4vc_certificate.credential,
                    "schema_id": "Nej8DViZyVvfyaLqGgWUw2:2:Legal Personal Identification Data (LPID):2.0.0",
                    "cred_def_id": "Nej8DViZyVvfyaLqGgWUw2:3:CL:84:default",
                    "rev_reg_id": None,
                    "cred_rev_id": None,
                    "credentialJwt": ready_oid4vc_certificate.credentialJwt,
                }
            )
    return Response(certificate_response, status=response.status_code)


def get_real_estate_insurance_certificate():
    organisation_id = config.FRIA_FORSAKRINGAR_ORG_ID
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
    api_key = config.FRIA_FORSAKRINGAR_API_KEY
    real_estate_insurance_cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG[
        "REAL_ESTATE_INSURANCE_CREDENTIAL_DEFINITION_ID"
    ]
    real_estate_insurance_connection_id = config.WALLET_USER_ISSUANCE_CONFIG[
        "REAL_ESTATE_INSURANCE_CONNECTION_ID"
    ]
    real_estate_insurance_data_agreement_id = (
        config.WALLET_USER_ISSUANCE_CONFIG[
            "REAL_ESTATE_INSURANCE_DATA_AGREEMENT_ID"
        ]
    )
    payload = {
        "comment": "Real estate insurance",
        "auto_remove": False,
        "trace": False,
        "cred_def_id": real_estate_insurance_cred_def_id,
        "connection_id": real_estate_insurance_connection_id,
        "credential_preview": {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
            "attributes": [
                {"name": "Insurance number", "value": "SR-234-01-F"},
                {"name": "Org. number", "value": "123400-7899"},
                {"name": "Name", "value": "Bygg AB"},
                {"name": "Validity date", "value": "2023-11-30"},
            ],
        },
        "auto_issue": True,
        "data_agreement_id": real_estate_insurance_data_agreement_id,
    }
    return url, api_key, payload


def get_ecolabel_certificate():
    organisation_id = config.ORNEN_ORG_ID
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
    api_key = config.ORNEN_API_KEY
    ecolabel_cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG[
        "ECOLABEL_CREDENTIAL_DEFINITION_ID"
    ]
    ecolabel_connection_id = config.WALLET_USER_ISSUANCE_CONFIG[
        "ECOLABEL_CONNECTION_ID"
    ]
    ecolabel_data_agreement_id = config.WALLET_USER_ISSUANCE_CONFIG[
        "ECOLABEL_DATA_AGREEMENT_ID"
    ]
    payload = {
        "comment": "Ecolabel",
        "auto_remove": False,
        "trace": False,
        "cred_def_id": ecolabel_cred_def_id,
        "connection_id": ecolabel_connection_id,
        "credential_preview": {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
            "attributes": [{"name": "License number", "value": "3019 2143"}],
        },
        "auto_issue": True,
        "data_agreement_id": ecolabel_data_agreement_id,
    }
    return url, api_key, payload


def get_default_certificate():
    organisation_id = config.BOLAGSVERKET_ORG_ID
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/issue-credential/send-offer"
    api_key = config.BYGG_AB_API_KEY
    cred_def_id = config.WALLET_USER_ISSUANCE_CONFIG["CREDENTIAL_DEFINITION_ID"]
    connection_id = config.WALLET_USER_ISSUANCE_CONFIG["CONNECTION_ID"]
    data_agreement_id = config.WALLET_USER_ISSUANCE_CONFIG["DATA_AGREEMENT_ID"]
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
                {
                    "name": "registeredAddress.thoroughFare",
                    "value": "Sveavägen",
                },
                {"name": "registeredAddress.locatorDesignator", "value": "48"},
                {"name": "registeredAddress.postCode", "value": "111 34"},
                {"name": "registeredAddress.postName", "value": "Stockholm"},
                {"name": "registeredAddress.adminUnitLevel1", "value": "SE"},
                {"name": "orgNumber", "value": "123400-7899"},
            ],
        },
        "auto_issue": True,
    }
    return url, api_key, payload


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def request_certificates(request):
    certificate = request.GET.get("certificate")

    def get_response(url, api_key, payload):
        response = requests.post(
            url,
            headers={
                "Authorization": api_key,
                "content-type": "application/json;charset=UTF-8",
            },
            json=payload,
        )
        status_code = response.status_code
        if response.status_code == 200:
            instance = Certificates.objects.create(
                user=request.user,
                credential_exchange_id=response.json().get(
                    "credential_exchange_id"
                ),
            )
            instance.save()
            response = response.json()
        else:
            response = response.text
        return response, status_code

    # Delete all the pending credential requests
    pending_oid4vc_certificates = OpenID4VCCertificate.objects.filter(
        status="pending"
    )
    pending_oid4vc_certificates.delete()

    if certificate == "real_estate_insurance":
        url, api_key, payload = get_real_estate_insurance_certificate()
        response, status_code = get_response(url, api_key, payload)
    elif certificate == "ecolabel":
        url, api_key, payload = get_ecolabel_certificate()
        response, status_code = get_response(url, api_key, payload)
    elif certificate == "all":
        url, api_key, payload = get_real_estate_insurance_certificate()
        real_estate_insurance_certificate, status_code = get_response(
            url, api_key, payload
        )
        url, api_key, payload = get_ecolabel_certificate()
        ecolabel_certificate, status_code = get_response(url, api_key, payload)
        url, api_key, payload = get_default_certificate()
        default_certificate, status_code = get_response(url, api_key, payload)
        responses = {
            "default_certificate": default_certificate,
            "real_estate_insurance_certificate": real_estate_insurance_certificate,
            "ecolabel_certificate": ecolabel_certificate,
        }
        return Response(responses)
    elif certificate == "lpid":
        issue_credential_req_body = {
            "issuanceMode": "Deferred",
            "credentialDefinitionId": "c41fcf08-0fa0-41b3-b097-fc5ebdad6048",
        }
        issuance_response = requests.post(
            "https://demo-api.igrant.io/v2/config/digital-wallet/openid/sdjwt/credential/issue",
            headers={
                "Authorization": config.BOLAGSVERKET_API_KEY,
                "content-type": "application/json;charset=UTF-8",
            },
            json=issue_credential_req_body,
        )
        if issuance_response.status_code == 200:
            issuance_response_json = issuance_response.json()
            authorization_header = config.BYGG_AB_OPENID4VC_API_KEY
            offer_response = requests.post(
                "https://demo-api.igrant.io/v2/config/digital-wallet/openid/sdjwt/credential/receive",
                json={
                    "credentialOffer": issuance_response_json.get(
                        "credentialHistory", {}
                    ).get("credentialOffer", "")
                },
                headers={"Authorization": authorization_header},
            )
            if offer_response.status_code == 200:
                offer_response_json = offer_response.json()
                oid4vc_certificate = OpenID4VCCertificate.objects.create(
                    user=request.user,
                    acceptance_token=offer_response_json.get(
                        "credential", {}
                    ).get("credentialId", "nil"),
                )
                oid4vc_certificate.save()
                return Response({}, status=200)
            else:
                return Response(
                    {"error": "Failed to resolved the credential offer"},
                    status=400,
                )
        else:
            return Response({"error": "Failed to request issuance"}, status=400)
    else:
        url, api_key, payload = get_default_certificate()
        response, status_code = get_response(url, api_key, payload)

    return Response(response, status=status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def check_certificate(request):
    credential_exchange_id = request.GET["credential_exchange_id"]
    authorization = config.BYGG_AB_API_KEY
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
    authorization = config.BYGG_AB_API_KEY
    url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/v1/data-agreements?method_of_use=data-source&publish_flag=true&page=1&page_size=1000000"
    response = requests.get(
        url,
        headers={
            "Authorization": authorization,
            "content-type": "application/json;charset=UTF-8",
        },
    )
    certificate_schemas = response.json()
    if organisation_id == config.BOLAGSVERKET_ORG_ID:
        certificate_schemas.get("results").insert(
            0,
            {
                "data_agreement_id": "e53700ae-d782-470d-ad1c-98ca72fcdf92",
                "state": "PREPARATION",
                "method_of_use": "data-source",
                "data_agreement": {
                    "@context": "https://raw.githubusercontent.com/decentralised-dataexchange/automated-data-agreements/main/interface-specs/data-agreement-schema/v1/data-agreement-schema-context.jsonld",
                    "template_id": "e53700ae-d782-470d-ad1c-98ca72fcdf92",
                    "template_version": 8,
                    "data_controller_name": "Bolagsverket",
                    "data_controller_url": "https://bolagsverket.se/policy.html",
                    "purpose": "Legal Personal Identification Data (LPID)",
                    "purpose_description": "Issue Legal Personal Identification Data (LPID) to companies.",
                    "lawful_basis": "consent",
                    "method_of_use": "data-source",
                    "data_policy": {
                        "data_retention_period": 1,
                        "policy_URL": "https://igrant.io/policy_default.html",
                        "jurisdiction": "Stockholm, SE",
                        "industry_sector": "Government",
                        "geographic_restriction": "Europe",
                        "storage_location": "Europe",
                    },
                    "personal_data": [
                        {
                            "attribute_id": "afcb00b7-0e5a-4440-8b39-8659e89b5984",
                            "attribute_name": "identifier",
                            "attribute_sensitive": False,
                            "attribute_category": "",
                            "attribute_description": "Identifier",
                        },
                        {
                            "attribute_id": "8d207a78-a5cb-47c8-99be-a2735c0afec5",
                            "attribute_name": "legalName",
                            "attribute_sensitive": False,
                            "attribute_category": "",
                            "attribute_description": "Legal Name",
                        },
                    ],
                    "dpia": {
                        "dpia_date": "2024-04-06T15:33",
                        "dpia_summary_url": "https://privacyant.se/dpia_results.html",
                    },
                },
                "publish_flag": True,
                "delete_flag": False,
                "schema_id": "H3DW1MUWZyBkP5LG4rTYRH:2:Legal Personal Identification Data (LPID):8.0.0",
                "cred_def_id": "H3DW1MUWZyBkP5LG4rTYRH:3:CL:65770:default",
                "presentation_request": None,
                "is_existing_schema": False,
                "created_at": 1712311410,
                "updated_at": 1712311410,
            },
        )
    return Response(certificate_schemas, status=response.status_code)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_certificate_schema_attributes(request):
    organisation_id = request.GET["organisation_id"]
    schema_id = request.GET["schema_id"]
    authorization = config.BYGG_AB_API_KEY
    if (
        schema_id.strip()
        == "H3DW1MUWZyBkP5LG4rTYRH:2:Legal Personal Identification Data (LPID):8.0.0"
    ):
        res = {
            "schema": {
                "ver": "1.0",
                "id": "H3DW1MUWZyBkP5LG4rTYRH:2:Certificate Of Registration:8.0.0",
                "name": "Certificate Of Registration",
                "version": "8.0.0",
                "attrNames": ["identifier", "legalName"],
                "seqNo": 65770,
            }
        }
        return Response(res, status=200)
    else:
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/schemas/{schema_id}"
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
    authorization = config.BYGG_AB_API_KEY
    organisation_id = request.GET["organisation_id"]
    referent = request.GET["referent"]
    tbd_oid4vc_certificates = OpenID4VCCertificate.objects.filter(
        acceptance_token=referent
    )
    if tbd_oid4vc_certificates:
        tbd_oid4vc_certificates.delete()
        return Response(status=204)
    else:
        url = f"https://cloudagent.igrant.io/v1/{organisation_id}/admin/credential/{referent}"
        response = requests.delete(
            url,
            headers={
                "Authorization": authorization,
                "content-type": "application/json;charset=UTF-8",
            },
        )
        return Response(status=response.status_code)
