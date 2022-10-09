from django.db import models
from igrant_user.models import IGrantUser


# Create your models here.
class Invitations(models.Model):
    user = models.ForeignKey(IGrantUser, on_delete=models.DO_NOTHING)
    invitation_data = models.TextField(null=True)
    connection_id = models.CharField(max_length=256, db_index=True, unique=True)