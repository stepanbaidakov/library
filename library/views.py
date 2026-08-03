from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Author, Book, Borrow
from .paginators import MyPageNumberPaginator
from .permissions import IsModerator, IsOwner
from .serializers import AuthorSerializer, BookSerializer, BorrowSerializer

# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "author", "genre", "year"]
    pagination_class = MyPageNumberPaginator

    def get_permissions(self):
        if (
            self.action == "update"
            or self.action == "partial_update"
            or self.action == "destroy"
            or self.action == "create"
        ):
            self.permission_classes = [IsModerator, IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = MyPageNumberPaginator

    def get_permissions(self):
        if (
            self.action == "update"
            or self.action == "partial_update"
            or self.action == "destroy"
            or self.action == "create"
        ):
            self.permission_classes = [IsModerator, IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    pagination_class = MyPageNumberPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrow = self.get_object()
        borrow.return_book()
        return Response({"detail": "Книга возвращена."})

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]
        elif self.action == "partial_update":
            self.permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == "create":
            self.permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "return_book":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.groups.filter(name="moderators").exists():
                return Borrow.objects.all()

            return Borrow.objects.filter(user=self.request.user)
        else:
            return Borrow.objects.all()
