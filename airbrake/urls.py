from django.conf.urls import url

import views

urlpatterns = [
  url("js_error/$",views.js_error,name="js_error"),
]
