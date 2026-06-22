from typing import Annotated

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


User = get_user_model()


class Club(TimestampedModel):
    book_title = models.CharField(max_length=255, verbose_name=_("Book Title"), unique=True)
    book_authors = models.CharField(max_length=255, verbose_name=_("Book Authors"))
    publication_year = models.IntegerField(verbose_name=_("Publication Year"))
    description = models.TextField(verbose_name=_("Book Description"))

    telegram_chat_link = models.URLField(verbose_name=_("Link on Telegram chat"))

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
