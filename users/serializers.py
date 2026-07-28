from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from library.models import Borrow
from library.serializers import BorrowSerializer

from .models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    borrows = BorrowSerializer(many=True, read_only=True)
    borrows_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "full_name", "phone", "borrows", "borrows_count"]
        read_only_fields = ("id",)

    def get_borrows_count(self, obj):
        return Borrow.objects.filter(user=obj).count()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "full_name", "phone"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        uid = self.context["uid"]
        token = self.context["token"]

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Пользователь не найден.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Токен недействителен.")

        attrs["user"] = user
        return attrs
