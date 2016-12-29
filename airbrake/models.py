from django.conf import settings
from django.db import models
import jsonfield

STATUS_CHOICES = (
  ("new","new"),
  ("resolved","resolved"),
  ("watching","watching"),
)

class JSError(models.Model):
  data = jsonfield.JSONField()
  ip = models.CharField(max_length=20)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  created = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=16,choices=STATUS_CHOICES,default="new")
  notes = models.TextField(null=True,blank=True)
