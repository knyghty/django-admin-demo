from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.debug import default_urlconf

from . import views

urlpatterns = i18n_patterns(
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("congrats/", default_urlconf, name="congrats"),
    path("", views.redirect_to_admin),
)
