from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Tender, Requirement
from django.http import JsonResponse
from .serializers import TenderSerializer,RequirementSerializer
from seller.serializers import ResponsesSerializer, ResponseSerializer
from igrant_user.serializers import IGrantUsersSerializer
from django.views.decorators.csrf import csrf_exempt
from igrant_user.models import IGrantUser
from seller.models import Responses



# Create your views here.
def serialize_to_dict(*,queryset,serializer_cls,many=False) -> dict:
    serializer_obj = serializer_cls(queryset,many=many)
    return serializer_obj.data 

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def list_tenders(request):
    tenders = Tender.objects.all()
    result = []
    for tender in tenders:
        serializer = TenderSerializer(tender)
        tenderData = serializer.data
        requirement = Requirement.objects.filter(tender_id=tender.id).order_by("id")
        serializer = RequirementSerializer(requirement,many=True)
        requirementData = serializer.data
        tenderData['requirement'] = requirementData 
        document = []
        for requirement in requirementData:
            try:
                response = Responses.objects.filter(tender=tender.id,requirements=requirement["id"]).order_by("id").first()
            except Responses.DoesNotExist:
                response = None
            if response:
                supplier = response.supplier
                serializer = ResponsesSerializer(response)
                response = serializer.data
                document.append(response)
            if not response:
                pass
        tenderData['responses'] = document
        result.append(tenderData)
    return JsonResponse(result,safe=False)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_tender(request, tender_id):
    tender = get_object_or_404(Tender, pk=tender_id)
    serializer = TenderSerializer(tender)
    tenderData = serializer.data
    requirement = Requirement.objects.filter(tender_id=tender.id).order_by("id")
    serializer = RequirementSerializer(requirement, many=True)
    requirementData = serializer.data
    tenderData['requirement'] = requirementData
    document = []
    for requirement in requirementData:
        try:
            response = Responses.objects.filter(tender=tender.id,requirements=requirement["id"]).first()
        except Responses.DoesNotExist:
            response = None
        if response:
            supplier = response.supplier
            serializer = ResponsesSerializer(response)
            response = serializer.data
            document.append(response)
        if not response:
            pass
    tenderData['responses'] = document
    return JsonResponse(tenderData)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def publish_tender(request, tender_id):
    tender = get_object_or_404(Tender, pk=tender_id)
    tender.status = "PUBLISHED"
    tender.save()
    serializer = TenderSerializer(tender)
    tenderData = serializer.data
    requirement = Requirement.objects.filter(tender_id=tender.id).order_by("id")
    serializer = RequirementSerializer(requirement,many=True)
    requirementData = serializer.data
    tenderData['requirement'] = requirementData 
 
    return JsonResponse(tenderData)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_qualification_documents(request):
    response = {
        "qualification_documents": [
            {
                "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default",
                "issuer_label": "Bolagsverket, Sweden",
                "data_agreement_id": "974c628b-83c4-4a22-a8c0-7b42169248ef"
            }
        ]
    }
    return JsonResponse(response)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def v2_get_tender(request, tender_id):
    suppliers = IGrantUser.objects.filter(user_type=IGrantUser.UserType.SELLER)
    tender = get_object_or_404(Tender, pk=tender_id)
    res_tender = serialize_to_dict(queryset=tender,serializer_cls=TenderSerializer)
    requirements = Requirement.objects.filter(tender_id=tender.id).order_by("id")
    res_tender['requirement'] = serialize_to_dict(queryset=requirements,serializer_cls=RequirementSerializer,many=True)
    general_requirement = requirements.filter(category="General").first()
    res_supplier_responses = []
    responses = Responses.objects.filter(tender=tender.id).order_by("id")
    verification_status = False
    for supplier in suppliers:
        responses = Responses.objects.filter(tender=tender.id,supplier=supplier).order_by("id")
        responses_dict = serialize_to_dict(queryset=responses,serializer_cls=ResponseSerializer,many=True)
        verification_status = responses.filter(requirements=general_requirement,presentation_state="verified").exists()
        supplier_dict = serialize_to_dict(queryset=supplier,serializer_cls=IGrantUsersSerializer)
        responses = { "supplier": supplier_dict, "verification_status": verification_status, "responses": responses_dict}
        res_supplier_responses.append(responses)
    res_tender['responses'] = res_supplier_responses
    return JsonResponse(res_tender)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def v2_list_tenders(request):
    suppliers = IGrantUser.objects.filter(user_type=IGrantUser.UserType.SELLER)
    tenders = Tender.objects.all()
    result = []
    for tender in tenders:
        res_tender = serialize_to_dict(queryset=tender,serializer_cls=TenderSerializer)
        requirements = Requirement.objects.filter(tender_id=tender.id).order_by("id")
        res_tender['requirement'] = serialize_to_dict(queryset=requirements,serializer_cls=RequirementSerializer,many=True)
        general_requirement = requirements.filter(category="General").first()
        res_supplier_responses = []
        responses = Responses.objects.filter(tender=tender.id).order_by("id")
        verification_status = False
        for supplier in suppliers:
            responses = Responses.objects.filter(tender=tender.id,supplier=supplier).order_by("id")
            responses_dict = serialize_to_dict(queryset=responses,serializer_cls=ResponseSerializer,many=True)
            verification_status = responses.filter(requirements=general_requirement,presentation_state="verified").exists()
            supplier_dict = serialize_to_dict(queryset=supplier,serializer_cls=IGrantUsersSerializer)
            responses = { "supplier": supplier_dict, "verification_status": verification_status, "responses": responses_dict}
            res_supplier_responses.append(responses)
        res_tender['responses'] = res_supplier_responses
        result.append(res_tender)
    return JsonResponse(result,safe=False)