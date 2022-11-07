from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_jsonfield_backport.models import JSONField

from igrant_user.managers import IGrantUserManager


class IGrantUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        COMPANY = "COMPANY", _("Company")
        ISSUER = "ISSUER", _("Issuer")
        BUYER = "BUYER", _("Buyer")
        SELLER = "SELLER", _("Seller")

    class Orgs(models.TextChoices):
        DEFAULT = "NIL", _("Nil")
        RAKSA_OY = "RAKSA_OY", _("Raksa Oy, Finland")
        BYGG_AB = "BYGG_AB", _("Bygg Ab, Sweden")
        BOLAGSVERKET = "BOLAGSVERKET_AB", _("Bolagsverket Ab, Sweden")

    class OrgsVerificationStatus(models.TextChoices):
        UNVERIFIED = "UNVERIFIED", _("Unverified")
        VERIFIED = "VERIFIED", _("Verified")

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    fullname = models.CharField(max_length=250,unique=True,null=True)
    user_type = models.CharField(
        max_length=8, choices=UserType.choices, default=UserType.COMPANY
    )
    org = models.CharField(max_length=250, choices=Orgs.choices, default=Orgs.DEFAULT)
    org_verification_status = models.CharField(
        max_length=250,
        choices=OrgsVerificationStatus.choices,
        default=OrgsVerificationStatus.UNVERIFIED,
    )
    connection_id = models.CharField(max_length=250,unique=True,null=True )
    connection_state = models.CharField(max_length=250,null=True)
    presentation_exchange_id = models.CharField(max_length=250,unique=True,null=True)
    presentation_state = models.CharField(max_length=250,null=True)
    presentation_record = JSONField(default=[])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = IGrantUserManager()

    def __str__(self):
        return self.email
