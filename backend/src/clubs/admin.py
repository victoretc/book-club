from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.mail import send_mail
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from app.admin import ModelAdmin, admin
from clubs.models import Club, ClubRequest


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


@admin.register(ClubRequest)
class ClubRequestAdmin(ModelAdmin):
    list_display = (
        "book_title",
        "book_authors",
        "publication_year",
        "requester",
        "status",
        "get_created",
    )

    list_filter = ("status",)
    search_fields = ("book_title", "book_authors", "requester__username", "requester__email")
    raw_id_fields = ("requester",)
    readonly_fields = ("requester", "created", "modified")
    list_per_page = 25

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "book_title",
                    "book_authors",
                    "publication_year",
                    "description",
                    "requester",
                )
            },
        ),
        (
            _("Approval"),
            {
                "fields": (
                    "status",
                    "telegram_chat_link",
                    "max_chat_link",
                    "admin_comment",
                )
            },
        ),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[ClubRequest]:
        return super().get_queryset(request).select_related("requester")

    @admin.display(description=_("Created"), ordering="created")
    def get_created(self, obj: ClubRequest) -> str | None:
        if obj.created:
            return naturaltime(obj.created)

    def save_model(self, request: HttpRequest, obj: ClubRequest, form, change: bool) -> None:
        previous_status = None
        if change and obj.pk:
            previous_status = ClubRequest.objects.filter(pk=obj.pk).values_list("status", flat=True).first()

        obj.save()

        if obj.status == ClubRequest.Status.APPROVED and previous_status != ClubRequest.Status.APPROVED:
            self._approve(obj)
        elif obj.status == ClubRequest.Status.DECLINED and previous_status != ClubRequest.Status.DECLINED:
            self._notify_declined(obj)

    def _approve(self, request: ClubRequest) -> None:
        club, _created = Club.objects.get_or_create(
            book_title=request.book_title,
            defaults={
                "book_authors": request.book_authors,
                "publication_year": request.publication_year,
                "description": request.description,
                "telegram_chat_link": request.telegram_chat_link,
                "max_chat_link": request.max_chat_link,
                "owner": request.requester,
            },
        )
        club.members.add(request.requester)

        html_message = render_to_string(
            "email/club_request_approved.html",
            {"request": request},
        )
        send_mail(
            subject=_("Клуб «%(book_title)s» создан") % {"book_title": request.book_title},
            message=_("Клуб «%(book_title)s» создан. Присоединяйся к обсуждению!") % {"book_title": request.book_title},
            html_message=html_message,
            from_email=None,
            recipient_list=[request.requester.email],
            fail_silently=False,
        )

    def _notify_declined(self, request: ClubRequest) -> None:
        html_message = render_to_string(
            "email/club_request_declined.html",
            {"request": request},
        )
        send_mail(
            subject=_("Заявка на клуб «%(book_title)s» отклонена") % {"book_title": request.book_title},
            message=_("К сожалению, заявка на создание клуба «%(book_title)s» отклонена.") % {"book_title": request.book_title},
            html_message=html_message,
            from_email=None,
            recipient_list=[request.requester.email],
            fail_silently=False,
        )
