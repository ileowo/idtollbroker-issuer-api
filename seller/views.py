from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from buyer.serializers import TenderSerializer,RequirementSerializer
from igrant_user.models import IGrantUser
from buyer.models import Tender, Requirement
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_tender(request, tender_id):
    user = request.user
    tender = get_object_or_404(Tender, pk=tender_id)
    tender_name = tender.name
    buyer_id = tender.user.id
    buyer = get_object_or_404(IGrantUser, pk=buyer_id)
    buyer_name = buyer.org
    buyer_address = buyer.address
    buyer_country = buyer.country
    buyer_presentation_record = buyer.presentation_record
    requirement = Requirement.objects.filter(tender_id=tender.id)
    serializer = RequirementSerializer(requirement, many=True)
    requirement_data = serializer.data
    response = {
        "name": tender_name,
        "buyer":
        {
            "name": buyer_name, "address": buyer_address, "country": buyer_country
        },
        "presentation_record": buyer_presentation_record,
        "requirement": requirement_data
    } 
    return JsonResponse(response)
    
    
def verify_certificate(request):
    pass