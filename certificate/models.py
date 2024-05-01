from django.db import models

# Create your models here.

from igrant_user.models import IGrantUser
from django_jsonfield_backport.models import JSONField


# Create your models here.
class Certificates(models.Model):
    user = models.ForeignKey(IGrantUser, on_delete=models.DO_NOTHING)
    credential_exchange_id = models.CharField(
        max_length=256, db_index=True, unique=True
    )


class OpenID4VCCertificate(models.Model):
    user = models.ForeignKey(IGrantUser, on_delete=models.CASCADE)
    acceptance_token = models.CharField(max_length=256, null=True, blank=True)
    credential = JSONField(default={}, blank=True)
    status = models.CharField(
        max_length=250, null=False, blank=False, default="pending"
    )
    createdAt = models.DateTimeField(auto_now_add=True)
