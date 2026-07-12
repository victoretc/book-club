from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from a12n.models import EmailVerificationCode


class TokenObtainPairWithProperMessageSerializer(TokenObtainPairSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    default_error_messages = {"no_active_account": _("Invalid username or password.")}


class TokenBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)


class RequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    detail = serializers.CharField(read_only=True)


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(max_length=4, min_length=4, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        code = data["code"]
        email = data["email"]

        try:
            instance = EmailVerificationCode.objects.filter(
                email=email, code=code, is_used=False
            ).latest("created_at")
        except EmailVerificationCode.DoesNotExist:
            raise serializers.ValidationError(
                {"code": "Неверный код подтверждения"}, code="invalid_code"
            )

        if instance.is_expired:
            raise serializers.ValidationError(
                {"code": "Срок действия кода истёк"}, code="code_expired"
            )

        data["instance"] = instance
        return data


class RetrieveCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email адрес, на который был отправлен код")

    def validate_email(self, value):
        if not EmailVerificationCode.objects.filter(email=value, is_used=False).exists():
            raise serializers.ValidationError("Нет активных кодов для этого email")
        return value


class RetrieveCodeResponseSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, help_text="4-значный код подтверждения")
