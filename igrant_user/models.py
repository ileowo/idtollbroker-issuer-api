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
        BYGG_AB = "BYGG_AB", _("Bygg AB, Sweden")
        BOLAGSVERKET = "BOLAGSVERKET_AB", _("Bolagsverket AB, Sweden")
        STHLM_CONSTRUCTIONS_AB = "STHLM_CONSTRUCTIONS_AB", _("Sthlm Constructions AB")
        RAPID_BUILDERS = "RAPID_BUILDERS", _("Rapid Builders")

    class OrgsVerificationStatus(models.TextChoices):
        UNVERIFIED = "UNVERIFIED", _("Unverified")
        VERIFIED = "VERIFIED", _("Verified")

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    fullname = models.CharField(max_length=250,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    country = models.CharField(max_length=250,null=True,blank=True)
    user_type = models.CharField(
        max_length=8, choices=UserType.choices, default=UserType.COMPANY
    )
    org = models.CharField(max_length=250, choices=Orgs.choices, default=Orgs.DEFAULT)
    org_verification_status = models.CharField(
        max_length=250,
        choices=OrgsVerificationStatus.choices,
        default=OrgsVerificationStatus.UNVERIFIED,
    )
    connection_id = models.CharField(max_length=250,unique=True,null=True,blank=True)
    connection_state = models.CharField(max_length=250,null=True,blank=True)
    presentation_exchange_id = models.CharField(max_length=250,unique=True,null=True,blank=True)
    presentation_state = models.CharField(max_length=250,null=True,blank=True)
    presentation_record = JSONField(default=[],blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = IGrantUserManager()

    def __str__(self):
        return self.email
