from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.api.request import AuthenticatedRequest
from users.api.serializers import UserRegisterSerializer, UserSerializer
from users.api.services import UserRegisterService
from users.models import User


class SelfView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    request: AuthenticatedRequest

    def get(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def delete(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_creator = UserRegisterService(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        user = user_creator()

        user_serializer = UserSerializer(user, context=self.get_serializer_context())
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
