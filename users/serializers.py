from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache


CustomUser = get_user_model()


class OAuthCoderializer(serializers.Serializer):
    code = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['birthdate'] = str(user.birthdate) if user.birthdate else None
        return token
    

class UserBaseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    birthdate = serializers.DateField(required=False)
    def validate_username(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('CustomUser уже существует!')


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('CustomUser не существует!')

        saved_code = cache.get(f"confirmation_code:{user_id}")

        if saved_code is None:
            raise ValidationError('Код подтверждения не найден или истёк!')

        if saved_code != code:
            raise ValidationError('Неверный код подтверждения!')

        return attrs