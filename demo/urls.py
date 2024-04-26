from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
