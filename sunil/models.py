from django.db import models

# Create your models here.
class Shope(models.Model):
    shope_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    