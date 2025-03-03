from django.contrib import admin

from demo.models import Artist
from demo.models import Release
from demo.models import ReleaseTrack
from demo.models import Track


class ReleaseInline(admin.StackedInline):
    model = Release


class ReleaseTrackInline(admin.TabularInline):
    autocomplete_fields = ["track"]
    fields = ["track_number", "track"]
    model = ReleaseTrack


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [ReleaseInline]
    readonly_fields = ["id"]
    search_fields = ["name"]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    date_hierarchy = "release_date"
    inlines = [ReleaseTrackInline]
    list_display = ["title", "artist", "type", "release_date"]
    list_editable = ["type", "release_date"]
    list_filter = ["type"]
    raw_id_fields = ["artist"]
    readonly_fields = ["id"]
    search_fields = ["title", "artist__name"]


@admin.register(ReleaseTrack)
class ReleaseTrackAdmin(admin.ModelAdmin):
    autocomplete_fields = ["release", "track"]
    search_fields = ["release__title", "track__title", "release__artist__name"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    search_fields = ["artists__name", "title"]
