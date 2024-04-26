from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = i18n_patterns(
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    prefix_default_language=False,
)
