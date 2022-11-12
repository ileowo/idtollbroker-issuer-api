from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Tender, Requirement
from django.http import JsonResponse
from .serializers import TenderSerializer,RequirementSerializer
from seller.serializers import ResponsesSerializer
from igrant_user.serializers import IGrantUsersSerializer
from django.views.decorators.csrf import csrf_exempt
from igrant_user.models import IGrantUser
from seller.models import Responses
import requests
import json


# Create your views here.
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def list_tenders(request):
    tenders = Tender.objects.all()
    result = []
    for tender in tenders:
        serializer = TenderSerializer(tender)
        tenderData = serializer.data
        requirement = Requirement.objects.filter(tender_id=tender.id)
        serializer = RequirementSerializer(requirement,many=True)
        requirementData = serializer.data
        tenderData['requirement'] = requirementData 
        document = []
        for requirement in requirementData:
            try:
                response = Responses.objects.get(tender=tender.id,requirements=requirement["id"])
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
    requirement = Requirement.objects.filter(tender_id=tender.id)
    serializer = RequirementSerializer(requirement, many=True)
    requirementData = serializer.data
    tenderData['requirement'] = requirementData
    document = []
    for requirement in requirementData:
        try:
            response = Responses.objects.get(tender=tender.id,requirements=requirement["id"])
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
    requirement = Requirement.objects.filter(tender_id=tender.id)
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



