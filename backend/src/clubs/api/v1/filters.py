import django_filters
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
)
from django.db.models import QuerySet

from clubs.models import BookReview, Category, Club


User = get_user_model()


class ReviewFilter(django_filters.FilterSet):
    club = django_filters.NumberFilter(field_name="club")

    class Meta:
        model = BookReview
        fields = ["club"]


class ClubFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    membership = django_filters.CharFilter(method="filter_by_membership")
    category = django_filters.NumberFilter(method="filter_by_category")
    club_type = django_filters.CharFilter(field_name="club_type")

    class Meta:
        model = Club
        fields: list[str] = []

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        if not value:
            return queryset

        return queryset.annotate(
            search=SearchVector("book_title", "author_name", config="russian"),
        ).filter(search=SearchQuery(value, config="russian"))

    def filter_by_membership(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()

        if value == "member":
            return queryset.filter(members=user)
        if value == "owner":
            return queryset.filter(owner=user)
        return queryset

    def filter_by_category(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        try:
            category = Category.objects.get(pk=value)
        except Category.DoesNotExist:
            return queryset.none()

        category_ids = [category.pk, *category.children.values_list("pk", flat=True)]
        return queryset.filter(category_id__in=category_ids)
