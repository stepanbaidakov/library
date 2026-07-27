from django.contrib.auth import get_user_model

from rest_framework import serializers

from library.models import Borrow
from library.serializers import BorrowSerializer

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    borrows = BorrowSerializer(many=True, read_only=True)
    borrows_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "full_name", "phone", "borrows", "borrows_count"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_borrows_count(self, obj):
        return Borrow.objects.filter(user=obj).count()

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, attrs):
        username = attrs.get("username", self.instance.username if self.instance else None)
        email = attrs.get("email", self.instance.username if self.instance else None)
        qs = CustomUser.objects.filter(username__iexact=username, email__iexact=email)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return attrs
