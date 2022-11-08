from rest_framework import generics
from .models import IGrantUser
from .serializers import IGrantUserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


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


@permission_classes([permissions.IsAdminUser])
@api_view(["POST"])
def AdminResetConnection(request):
    queryset = IGrantUser.objects.all()
    for user in queryset:
        user.connection_id = None
        user.connection_state = None
        user.presentation_exchange_id = None
        user.presentation_state = None
        user.presentation_record = []
        user.save()
    return HttpResponse(status=status.HTTP_200_OK)
