from django.core.validators import EmailValidator
from rest_framework import serializers

from a12n.models import EmailVerificationCode


class RequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4, min_length=4)

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
