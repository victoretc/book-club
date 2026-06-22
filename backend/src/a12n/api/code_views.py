from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from a12n.api.code_serializers import RequestCodeSerializer, VerifyCodeSerializer
from a12n.api.throttling import AuthAnonRateThrottle
from a12n.models import EmailVerificationCode
from users.models import User


class RequestCodeView(GenericAPIView):
    serializer_class = RequestCodeSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthAnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        EmailVerificationCode.objects.filter(email=email, is_used=False).update(
            is_used=True
        )
        code = EmailVerificationCode.create_for_email(email)

        html_message = render_to_string("email/code_email.html", {"code": code.code})
        send_mail(
            subject="Вход в Читальную",
            message=f"Ваш код: {code.code}",
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"detail": "Код отправлен на вашу почту"}, status=status.HTTP_200_OK)


class VerifyCodeView(GenericAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthAnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        instance = serializer.validated_data["instance"]

        instance.is_used = True
        instance.save(update_fields=["is_used"])

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "is_active": True,
            },
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )
