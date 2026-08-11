from typing import ClassVar

from django.contrib.auth.models import AbstractUser, UserManager as _UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    objects: ClassVar[_UserManager] = _UserManager()
    is_reading_list_public = models.BooleanField(default=False, db_default=False, verbose_name=_("Reading list is public"))
