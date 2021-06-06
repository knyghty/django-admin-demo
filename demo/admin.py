from django.contrib import admin

from demo.models import Artist, Release, ReleaseTrack, Track


class ReleaseInline(admin.StackedInline):
    model = Release


class ReleaseTrackInline(admin.TabularInline):
    fields = ["track_number", "track"]
    model = ReleaseTrack


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [ReleaseInline]
    readonly_fields = ["id"]
    search_fields = ["name"]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    autocomplete_fields = ["artist"]
    date_hierarchy = "release_date"
    inlines = [ReleaseTrackInline]
    list_display = ["title", "artist", "type", "release_date"]
    list_editable = ["type", "release_date"]
    list_filter = ["type"]
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
