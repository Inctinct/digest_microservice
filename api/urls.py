from django.urls import path, re_path

from api.views import DigestView

urlpatterns = [re_path("digest/", DigestView.as_view())]
