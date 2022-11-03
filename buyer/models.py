from django.db import models

# Create your models here.
class Tender(models.Model):


    class STATUS(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ISSUER = "PUBLISHED", "Published"

        
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=16, choices=STATUS.choices, default=STATUS.DRAFT)


    def __str__(self):
        return self.name


class Requirement(models.Model):
    id = models.BigIntegerField(primary_key=True,unique = True)
    category = models.CharField(max_length=256)
    requirement_header = models.CharField(max_length=256)
    requirement_description = models.CharField(max_length=256)
    requirement_category = models.CharField(max_length=256)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.category