from django.db import models
from django_jsonfield_backport.models import JSONField
from buyer.models import Tender, Requirement
from igrant_user.models import IGrantUser


# Create your models here.
class Responses(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, blank=True, null=True)
    requirements = models.ForeignKey(Requirement, on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey(IGrantUser, on_delete=models.CASCADE, blank=True, null=True)
    presentation_exchange_id = models.CharField(max_length=250,unique=True,null=True,blank=True)
    presentation_state = models.CharField(max_length=250,null=True,blank=True)
    presentation_record = JSONField(default=[],blank=True)
    
    