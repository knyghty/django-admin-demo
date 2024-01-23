from datetime import date

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from demo.models import Artist, Release, ReleaseTrack, Track


class ReleaseInline(admin.StackedInline):
    model = Release


class ReleaseTrackInline(admin.TabularInline):
    fields = ["track_number", "track"]
    model = ReleaseTrack


class PeriodReleaseListFilter(admin.SimpleListFilter):
    title = _("Period release")

    parameter_name = "period"

    def lookups(self, request, model_admin):
        return [
            ("pre 80s", _("pre eighties")),
            ("1980s", _("in the eighties")),
            ("1990s", _("in the nineties")),
            ("2000s", _("in the aughts")),
            ("2010s", _("in the twenty tens")),
            ("2020s", _("in the twenty twenties")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "pre 80s":
            return queryset.filter(
                release_date__lte=date(1979, 12, 31),
            )
        if self.value() == "1980s":
            return queryset.filter(
                release_date__gte=date(1980, 1, 1),
                release_date__lte=date(1989, 12, 31),
            )
        if self.value() == "1990s":
            return queryset.filter(
                release_date__gte=date(1990, 1, 1),
                release_date__lte=date(1999, 12, 31),
            )
        if self.value() == "2000s":
            return queryset.filter(
                release_date__gte=date(2000, 1, 1),
                release_date__lte=date(2009, 12, 31),
            )
        if self.value() == "2010s":
            return queryset.filter(
                release_date__gte=date(2010, 1, 1),
                release_date__lte=date(2019, 12, 31),
            )
        if self.value() == "2020s":
            return queryset.filter(
                release_date__gte=date(2020, 1, 1),
                release_date__lte=date(2029, 12, 31),
            )


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
    list_filter = ["type", PeriodReleaseListFilter]
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
