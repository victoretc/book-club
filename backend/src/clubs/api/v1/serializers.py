from django.contrib.auth import get_user_model
from rest_framework import serializers

from clubs.models import BookReview, Club


User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BookReview
        fields = ["id", "club", "user", "review", "assessment", "read_pages", "created", "modified"]
        read_only_fields = ["created", "modified", "id"]


class ClubSerializer(serializers.ModelSerializer):
    reviews = BookReviewSerializer(many=True, read_only=True)
    owner: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(read_only=True)
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = [
            "id",
            "book_title",
            "book_authors",
            "publication_year",
            "description",
            "telegram_chat_link",
            "owner",
            "members",
            "reviews",
            "created",
            "modified",
        ]
        read_only_fields = ["owner", "members", "created", "modified", "id"]
