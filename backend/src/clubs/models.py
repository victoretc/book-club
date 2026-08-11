from typing import Annotated, Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


User = get_user_model()


class Category(TimestampedModel):
    name = models.CharField(max_length=120, unique=True, verbose_name=_("Name"))
    slug = models.SlugField(max_length=140, unique=True, blank=True, verbose_name=_("Slug"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent Category"),
    )
    position = models.PositiveIntegerField(default=0, verbose_name=_("Position"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name

    @property
    def full_path(self) -> str:
        parts = [self.name]
        parent = self.parent
        while parent is not None:
            parts.append(parent.name)
            parent = parent.parent
        return " / ".join(reversed(parts))

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Club(TimestampedModel):
    book_title = models.CharField(max_length=255, verbose_name=_("Book Title"), unique=True)
    book_authors = models.CharField(max_length=255, verbose_name=_("Book Authors"))
    publication_year = models.IntegerField(verbose_name=_("Publication Year"))
    description = models.TextField(verbose_name=_("Book Description"))

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clubs",
        verbose_name=_("Category"),
    )

    telegram_chat_link = models.URLField(verbose_name=_("Link on Telegram chat"))
    max_chat_link = models.URLField(blank=True, verbose_name=_("Link on Max chat"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_clubs", verbose_name=_("Club Owner"))

    members: models.ManyToManyField = models.ManyToManyField(User, related_name="clubs", blank=True, verbose_name=_("Members"))

    member_count: Annotated[int, models.Count]

    class Meta:
        verbose_name = _("Book Club")
        verbose_name_plural = _("Book Clubs")
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{_('Club')} '{self.book_title}'"


class BookReview(TimestampedModel):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField(verbose_name=_("Book Review"))
    assessment = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_("Assessment"))
    read_pages = models.IntegerField(verbose_name=_("Read Pages"))

    class Meta:
        constraints = [models.UniqueConstraint(fields=["club", "user"], name="unique_user_review_per_club")]
        ordering = ["-created"]
        verbose_name = _("Book Review")
        verbose_name_plural = _("Book Reviews")

    def __str__(self) -> str:
        return _("Review by %(username)s for %(club_name)s") % {"username": self.user.username, "club_name": self.club.book_title}


class ClubRequest(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        DECLINED = "declined", _("Declined")

    book_title = models.CharField(max_length=255, verbose_name=_("Book Title"))
    book_authors = models.CharField(max_length=255, verbose_name=_("Book Authors"))
    publication_year = models.IntegerField(verbose_name=_("Publication Year"))
    description = models.TextField(verbose_name=_("Book Description"))

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="club_requests",
        verbose_name=_("Category"),
    )

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="club_requests", verbose_name=_("Requester"))

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, verbose_name=_("Status"))

    telegram_chat_link = models.URLField(blank=True, verbose_name=_("Link on Telegram chat"))
    max_chat_link = models.URLField(blank=True, verbose_name=_("Link on Max chat"))
    admin_comment = models.TextField(blank=True, verbose_name=_("Admin Comment"))

    class Meta:
        verbose_name = _("Club Request")
        verbose_name_plural = _("Club Requests")
        ordering = ["-created"]

    def clean(self) -> None:
        if self.status == self.Status.APPROVED and not self.telegram_chat_link:
            raise ValidationError({"telegram_chat_link": _("Telegram chat link is required to approve the request.")})

    def __str__(self) -> str:
        return _("Request for '%(book_title)s'") % {"book_title": self.book_title}
