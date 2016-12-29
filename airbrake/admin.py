from django.contrib import admin

from .models import JSError

import json

@admin.register(JSError)
class JSErrorAdmin(admin.ModelAdmin):
  raw_id_fields = ("user",)
  fields = ("user","ip","_data",)
  readonly_fields = ("_data",)
  def _data(self,obj):
    lines = []
    for k,v in sorted(obj.data.items()):
      if v:
        lines.append("<h4>%s</h4><pre>%s</pre>"%(k,json.dumps(v,sort_keys=True, indent=4)))
    return "".join(lines)
  _data.allow_tags = True
