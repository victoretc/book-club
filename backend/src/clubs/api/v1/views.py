from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from clubs.api.v1.filters import ClubFilter, ReviewFilter
from clubs.api.v1.serializers import BookClubRequestSerializer, BookReviewSerializer, ClubSerializer
from clubs.models import BookReview, Club, ClubRequest


User = get_user_model()


class IsClubOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Club) -> bool:
        return obj.owner == request.user


class IsReviewAuthor(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: BookReview) -> bool:
        return obj.user == request.user


class ClubViewSet(ModelViewSet):
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ClubFilter

    permission_classes_by_action: dict[str, list[type[permissions.BasePermission]] | Any] = {
        "create": [permissions.IsAuthenticated],
        "update": [IsClubOwner],
        "partial_update": [IsClubOwner],
        "destroy": [IsClubOwner],
    }

    def get_permissions(self) -> list[permissions.BasePermission]:
        try:
            permission_classes = self.permission_classes_by_action[self.action]
        except KeyError:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Club]:
        return (
            Club.objects.select_related("owner")
            .prefetch_related("members")
            .prefetch_related(Prefetch("reviews", queryset=BookReview.objects.select_related("user")))
        )

    def perform_create(self, serializer: BaseSerializer) -> None:
        club = serializer.save(owner=self.request.user)
        club.members.add(self.request.user)

    @extend_schema(methods=["POST"], request=None, responses={204: None})
    @extend_schema(methods=["DELETE"], request=None, responses={204: None})
    @action(detail=True, methods=["POST", "DELETE"], url_path="members/me")
    def manage_membership(self, request: Request, pk: int | None = None) -> Response:
        club = self.get_object()

        if request.method == "POST":
            if club.members.filter(pk=request.user.pk).exists():
                return Response({"detail": "User is already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)
            club.members.add(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == "DELETE":
            if club.owner == request.user:
                return Response({"detail": "Club owner cannot leave the club."}, status=status.HTTP_400_BAD_REQUEST)

            if not club.members.filter(pk=request.user.pk).exists():
                return Response({"detail": "User is not a member of this club."}, status=status.HTTP_400_BAD_REQUEST)

            club.members.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(ModelViewSet):
    serializer_class = BookReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ReviewFilter

    permission_classes_by_action: dict[str, list[type[permissions.BasePermission]] | Any] = {
        "update": [permissions.IsAuthenticated, IsReviewAuthor],
        "partial_update": [permissions.IsAuthenticated, IsReviewAuthor],
        "destroy": [permissions.IsAuthenticated, IsReviewAuthor],
    }

    def get_permissions(self) -> list[permissions.BasePermission]:
        try:
            permission_classes = self.permission_classes_by_action[self.action]
        except KeyError:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[BookReview]:
        return BookReview.objects.select_related("user", "club")

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user)


class ClubRequestViewSet(ModelViewSet):
    serializer_class = BookClubRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "post"]

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action == "create":
            return [permission() for permission in [permissions.IsAuthenticated]]
        return [permission() for permission in [permissions.IsAdminUser]]

    def get_queryset(self) -> QuerySet[ClubRequest]:
        return ClubRequest.objects.select_related("requester")

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(requester=self.request.user)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request: Request) -> Response:
        queryset = self.get_queryset().filter(requester=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
