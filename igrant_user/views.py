from rest_framework import generics
from .models import IGrantUser
from .serializers import IGrantUserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


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
