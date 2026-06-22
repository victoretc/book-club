from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


__all__ = [
    "DefaultModel",
    "TimestampedModel",
    "models",
]


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Default name for all models"""
        name = getattr(self, "name", None)
        if name is not None:
            return str(name)

        return super().__str__()

    @classmethod
    def get_contenttype(cls) -> ContentType:
        return ContentType.objects.get_for_model(cls)

    def update_from_kwargs(self, **kwargs: dict[str, Any]) -> None:
        """A shortcut method to update model instance from the kwargs."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def setattr_and_save(self, key: str, value: Any) -> None:
        """Shortcut for testing -- set attribute of the model and save"""
        setattr(self, key, value)
        self.save()

    @classmethod
    def get_label(cls) -> str:
        """Get a unique within the app model label"""
        return cls._meta.label_lower.split(".")[-1]


class Timestamped(models.Model):
    """
    An abstract behavior representing timestamping a model with``created`` and
    ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Дата создания"))
    modified = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name=_("Дата изменения"))

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk:
            self.modified = timezone.now()
        return super().save(*args, **kwargs)

    @property
    def changed(self) -> bool:
        return bool(self.modified)


class TimestampedModel(DefaultModel, Timestamped):
    """
    Default app model that has `created` and `updated` attributes.
    Currently based on https://github.com/audiolion/django-behaviors
    """

    class Meta:
        abstract = True
