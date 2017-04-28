from django.conf import settings
from django.db import models
import jsonfield

import httpagentparser

class UserAgentManager(models.Manager):
  def from_string(self,s):
    try:
      return self.get(string=s)
    except self.model.DoesNotExist:
      pass
    except ValueError:
      return None
    agent = httpagentparser.detect(s)
    kwargs = {}
    for key in ['browser','os','dist']:
      if key in agent:
        kwargs[key] = "@".join([agent[key]["name"],agent[key].get("version",'None')])
    return self.create(string=s,**kwargs)

class UserAgent(models.Model):
  browser = models.CharField(max_length=64)
  os = models.CharField(max_length=64,null=True,blank=True)
  dist = models.CharField(max_length=64,null=True,blank=True)
  string = models.TextField(help_text="The useragent string that generated this entry.")
  objects = UserAgentManager()
  __unicode__ = lambda self: " | ".join([self.browser,self.os or "Unknown",self.dist or "Unknown"])
  class Meta:
    ordering = ("browser","os")

STATUS_CHOICES = (
  ("new","new"),
  ("resolved","resolved"),
  ("watching","watching"),
)

class ErrorGroupManager(models.Manager):
  def from_data(self,data):
    error = data.get('errors',[{}])[0]
    file_line_column = "no backtrace?!"
    if error.get('backtrace',None):
      file_line_column = "{b[file]} {b[line]}@{b[column]}".format(b=error['backtrace'][0])
    obj = self.get_or_create(
      message=error.get('message',"no message!?")[:128],
      file_line_column=file_line_column,
    )[0]
    if data.get("context",{}).get("userAgent",None):
      ua = UserAgent.objects.from_string(data['context']["userAgent"])
      if ua:
        obj.useragents.add(ua)
        obj.save()
    return obj

class ErrorGroup(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  useragents = models.ManyToManyField(UserAgent)
  message = models.CharField(max_length=128)
  file_line_column = models.TextField()
  notes = models.TextField()
  status = models.CharField(max_length=16,choices=STATUS_CHOICES,default="new")
  objects = ErrorGroupManager()
  __unicode__ = lambda self: self.message
  class Meta:
    ordering = ("-modified",)

class JSError(models.Model):
  errorgroup = models.ForeignKey(ErrorGroup,null=True,blank=True)
  data = jsonfield.JSONField()
  ip = models.CharField(max_length=20)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  created = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=16,choices=STATUS_CHOICES,default="new")
  notes = models.TextField(null=True,blank=True)
  def save(self,*args,**kwargs):
    self.errorgroup = self.errorgroup or ErrorGroup.objects.from_data(self.data)
    super(JSError,self).save(*args,**kwargs)
