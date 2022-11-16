from rest_framework import generics
from .models import IGrantUser
from seller.models import Responses
from .serializers import IGrantUserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class UserList(generics.ListAPIView):
    serializer_class = IGrantUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        email = self.request.user.email
        return IGrantUser.objects.filter(email=email)


class UserDetail(generics.RetrieveAPIView):
    queryset = IGrantUser.objects.all()
    serializer_class = IGrantUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


@csrf_exempt
@permission_classes([permissions.IsAdminUser])
@api_view(["POST"])
def AdminReset(request):
    queryset = IGrantUser.objects.all()
    for user in queryset:
        user.connection_id = None
        user.connection_state = None
        user.org_verification_status = "UNVERIFIED"
        user.presentation_exchange_id = None
        user.presentation_state = None
        user.presentation_record = []
        user.save()
    queryset = Responses.objects.all()
    for responses in queryset:
        responses.presentation_exchange_id = None
        responses.presentation_state = "unverified"
        responses.presentation_record = []
        responses.save()
    return HttpResponse(status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([permissions.IsAdminUser])
@api_view(["POST"])
def UserReset(request):
    user = request.user
    user.connection_id = None
    user.connection_state = None
    user.org_verification_status = "UNVERIFIED"
    user.presentation_exchange_id = None
    user.presentation_state = None
    user.presentation_record = []
    user.save()
    queryset = Responses.objects.filter(supplier=user)
    for responses in queryset:
        responses.presentation_exchange_id = None
        responses.presentation_state = "unverified"
        responses.presentation_record = []
        responses.save()
    return HttpResponse(status=status.HTTP_200_OK)
