from django.contrib.auth import get_user_model
from rest_framework import serializers

from clubs.models import BookReview, Category, Club, ClubRequest


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        read_only_fields = fields


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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "club_type",
            "book_title",
            "book_authors",
            "publication_year",
            "description",
            "author_name",
            "author_bio",
            "author_photo",
            "category",
            "category_name",
            "telegram_chat_link",
            "max_chat_link",
            "owner",
            "members",
            "reviews",
            "created",
            "modified",
        ]
        read_only_fields = ["owner", "members", "created", "modified", "id", "category_name"]

    def get_category_name(self, obj: Club) -> str | None:
        return obj.category.name if obj.category else None

    def validate(self, attrs: dict) -> dict:
        club_type = attrs.get("club_type", getattr(self.instance, "club_type", Club.Type.BOOK))
        if club_type == Club.Type.AUTHOR:
            if not attrs.get("author_name"):
                raise serializers.ValidationError({"author_name": "Укажите имя автора/ведущего."})
            if not attrs.get("author_bio"):
                raise serializers.ValidationError({"author_bio": "Добавьте описание автора/ведущего."})
        return attrs


class BookClubRequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = ClubRequest
        fields = [
            "id",
            "club_type",
            "book_title",
            "book_authors",
            "publication_year",
            "description",
            "author_name",
            "author_bio",
            "author_photo",
            "category",
            "category_name",
            "status",
            "requester",
            "telegram_chat_link",
            "max_chat_link",
            "admin_comment",
            "created",
            "modified",
        ]
        read_only_fields = [
            "id",
            "status",
            "requester",
            "telegram_chat_link",
            "max_chat_link",
            "admin_comment",
            "created",
            "modified",
            "category_name",
        ]

    def get_category_name(self, obj: ClubRequest) -> str | None:
        return obj.category.name if obj.category else None

    def validate(self, attrs: dict) -> dict:
        club_type = attrs.get("club_type", Club.Type.BOOK)
        if club_type == Club.Type.AUTHOR:
            if not attrs.get("author_name"):
                raise serializers.ValidationError({"author_name": "Укажите имя автора/ведущего."})
            if not attrs.get("author_bio"):
                raise serializers.ValidationError({"author_bio": "Добавьте описание автора/ведущего."})
        return attrs
