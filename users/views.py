import random
import string
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import (
    AuthValidateSerializer,
    ConfirmationSerializer,
    RegisterValidateSerializer,
    CustomTokenObtainPairSerializer,

)
from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView
CustomUser = get_user_model()
from users.tasks import add


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        add(6,9)
        add.delay(6,9)
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"error": "CustomUser account is not activated yet!"},
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"key": token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={"error": "CustomUser credentials are wrong!"},
        )


class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterValidateSerializer
   

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        birthdate = serializer.validated_data["birthdate"]
        

        # Use transaction to ensure data consistency
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email, password=password, is_active=False, birthdate=birthdate
            )

            # Create a random 6-digit code
            code = "".join(random.choices(string.digits, k=6))

            cache.set(f"confirmation_code:{user.id}", code, timeout=300)

        return Response(
            status=status.HTTP_201_CREATED,
            data={"user_id": user.id, "confirmation_code": code},
        )


class ConfirmUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            cache.delete(f"confirmation_code:{user.id}")

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "CustomUser аккаунт успешно активирован",
                "key": token.key,
            },
        )