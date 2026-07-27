from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from library.permissions import IsModerator
from users.models import CustomUser
from users.serializers import UserSerializer

from .permissions import IsUser

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsUser)]
        if self.action == "update":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsUser)]
        if self.action == "partial_update":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsUser)]
        if self.action == "list":
            self.permission_classes = [IsAuthenticated, IsModerator]
        if self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsUser]
        return [permission() for permission in self.permission_classes]
