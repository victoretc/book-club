from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.api.pagination import AppPagination
from app.api.request import AuthenticatedRequest
from clubs.models import BookReview, Club
from users.api.serializers import (
    ReadingListBookSerializer,
    ReadingListResponseSerializer,
    ReadingListUserSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
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


class UserBooksView(GenericAPIView):
    serializer_class = ReadingListBookSerializer
    permission_classes = [AllowAny]
    pagination_class = AppPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("page", type=OpenApiTypes.INT, required=False),
            OpenApiParameter("page_size", type=OpenApiTypes.INT, required=False),
        ],
        responses=ReadingListResponseSerializer,
    )
    def get(self, request: Request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk, is_active=True)

        if not user.is_reading_list_public:
            raise NotFound(_("Reading list is hidden."))

        queryset = (
            Club.objects.filter(members=user)
            .select_related("owner")
            .prefetch_related(Prefetch("reviews", queryset=BookReview.objects.filter(user=user)))
            .order_by("id")
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        data = self.get_paginated_response(serializer.data).data
        data["user"] = ReadingListUserSerializer(user).data
        return Response(data)
