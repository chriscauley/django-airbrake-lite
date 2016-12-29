from django.conf import settings
from django.db import models
import jsonfield

class JSError(models.Model):
  data = jsonfield.JSONField()
  ip = models.CharField(max_length=20)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
