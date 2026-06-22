from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from app.admin import ModelAdmin, admin
from clubs.models import Club


@admin.register(Club)
class ClubAdmin(ModelAdmin):
    list_display = (
        "book_title",
        "book_authors",
        "publication_year",
        "member_count",
        "get_created",
        "get_modified",
    )

    list_filter = ("created",)
    search_fields = ("book_title", "book_authors", "owner__username", "owner__email")
    raw_id_fields = ("owner",)
    readonly_fields = ("created", "modified")
    list_per_page = 25

    def get_queryset(self, request: HttpRequest) -> QuerySet[Club]:
        return super().get_queryset(request).select_related("owner").prefetch_related("members").annotate(member_count=Count("members"))

    @admin.display(description=_("Members count"), ordering="member_count")
    def member_count(self, obj: Club) -> int:
        return obj.member_count

    @admin.display(description=_("Update Date"), ordering="modified")
    def get_modified(self, obj: Club) -> str:
        if obj.modified:
            return naturaltime(obj.modified)
        return "—"

    @admin.display(description=_("Created"), ordering="created")
    def get_created(self, obj: Club) -> str | None:
        if obj.created:
            return naturaltime(obj.created)
