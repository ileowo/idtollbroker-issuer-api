from django.db import models

# Create your models here.

from igrant_user.models import IGrantUser


# Create your models here.
class Certificates(models.Model):
    user = models.ForeignKey(IGrantUser, on_delete=models.DO_NOTHING)
    credential_exchange_id = models.CharField(max_length=256, db_index=True, unique=True)
