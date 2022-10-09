from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import IGrantUserManager


class IGrantUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        COMPANY = 'COMPANY', _('Company')
        ISSUER = 'ISSUER', _('Issuer')

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(max_length=8, choices=UserType.choices, default=UserType.COMPANY)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = IGrantUserManager()

    def __str__(self):
        return self.email
