import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone


CODE_EXPIRY = timedelta(minutes=10)


class EmailVerificationCodeManager(models.Manager):
    def clean_expired(self) -> int:
        deadline = timezone.now() - CODE_EXPIRY
        deleted, _ = self.filter(created_at__lt=deadline).delete()
        return deleted


class EmailVerificationCode(models.Model):
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    objects = EmailVerificationCodeManager()

    class Meta:
        indexes = [
            models.Index(fields=["email", "code"]),
        ]

    def __str__(self) -> str:
        return f"{self.email}: {self.code}"

    @property
    def is_expired(self) -> bool:
        return timezone.now() - self.created_at > CODE_EXPIRY

    @classmethod
    def generate_code(cls) -> str:
        return f"{secrets.randbelow(10000):04d}"

    @classmethod
    def create_for_email(cls, email: str) -> "EmailVerificationCode":
        return cls.objects.create(email=email, code=cls.generate_code())
