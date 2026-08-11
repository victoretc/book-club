from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from clubs.models import BookReview, Club
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    remote_addr = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_reading_list_public",
            "remote_addr",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def get_remote_addr(self, obj: User) -> str:
        return self.context["request"].META["REMOTE_ADDR"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class ReadingListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class ReadingListReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["id", "review", "assessment", "read_pages", "created"]


class ReadingListBookSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ["id", "book_title", "book_authors", "publication_year", "description", "review"]

    @extend_schema_field(ReadingListReviewSerializer(allow_null=True))
    def get_review(self, obj: Club) -> dict | None:
        review = obj.reviews.first()
        if review is None:
            return None
        return ReadingListReviewSerializer(review).data


class ReadingListResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True, required=False)
    previous = serializers.CharField(allow_null=True, required=False)
    user = ReadingListUserSerializer()
    results = ReadingListBookSerializer(many=True)
