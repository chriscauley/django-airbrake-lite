from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from .models import JSError
import json

@csrf_exempt
def js_error(request):
  if not 'data' in request.POST:
    raise Http404()
  if "Googlebot" in request.POST['data'].get("userAgent",""):
    raise Http404()
  user = request.user if request.user.is_authenticated() else None
  JSError.objects.create(
    data=json.loads(request.POST['data']),
    ip=request.META.get('HTTP_X_REAL_IP',"None"),
    user=user
  )
  return HttpResponse("z?")
