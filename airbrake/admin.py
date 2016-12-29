from django.contrib import admin

from .models import JSError

import json

@admin.register(JSError)
class JSErrorAdmin(admin.ModelAdmin):
  raw_id_fields = ("user",)
  fields = ("user","ip","_data",)
  readonly_fields = ("_data",)
  list_display = ("user","created","url","message")
  def _data(self,obj):
    lines = []
    for k,v in sorted(obj.data.items()):
      if v:
        lines.append("<h4>%s</h4><pre>%s</pre>"%(k,json.dumps(v,sort_keys=True, indent=4)))
    return "".join(lines)
  _data.allow_tags = True
  def url(self,obj):
    return obj.data.get("context",{}).get("url","No Url")
  def message(self,obj):
    errors = obj.data.get("errors",[])
    if not errors:
      return "no errors?!"
    return "<br/>".join([e.get('message',"No message!?") for e in errors])
  message.allow_tags = True
