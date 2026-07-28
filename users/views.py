from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from library.permissions import IsModerator
from users.models import CustomUser
from users.serializers import UserSerializer, UserCreateSerializer
from .permissions import IsUser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.mail import send_mail

from django.urls import reverse

from django.utils.encoding import force_bytes
from django.utils.http import (
    urlsafe_base64_encode,
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)

# Create your views here.

User = get_user_model()


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

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        else:
            return UserSerializer


class PasswordResetView(APIView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = request.build_absolute_uri(
            reverse("users:password-reset-confirm", kwargs={"uidb64": uid, "token": token})
        )
        send_mail(
            subject="Восстановление пароля",
            message=f"""
Здравствуйте.
Для восстановления пароля перейдите по ссылке
{reset_url}
Если это были не Вы — проигнорируйте письмо.
""",
            from_email=None,
            recipient_list=[email],
        )
        return Response(
            {"detail": "Письмо отправлено"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(
            data=request.data,
            context={
                "uid": uidb64,
                "token": token,
            },
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Пароль успешно изменён"}
        )
