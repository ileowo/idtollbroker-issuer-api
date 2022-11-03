from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Tender, Requirement
from django.http import JsonResponse
from .serializers import TenderSerializer,RequirementSerializer

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def list_tenders(request):
    tenders = Tender.objects.all()
    response = []
    for tender in tenders:
        serializer = TenderSerializer(tender)
        tenderData = serializer.data
        requirement = Requirement.objects.filter(tender_id=tender.id)
        serializer = RequirementSerializer(requirement,many=True)
        requirementData = serializer.data
        tenderData['requirement'] = requirementData 
        response.append(tenderData )

    return JsonResponse(response,safe=False)


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
    return JsonResponse(tenderData)


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