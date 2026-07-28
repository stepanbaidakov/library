from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet
from .views import (
    PasswordResetView,
    PasswordResetConfirmView,
)

app_name = "users"

router = DefaultRouter()
router.register("profile", UserViewSet, basename="profile")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset",),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm",),
] + router.urls
