import collections
import datetime
import pprint

import spotipy
from django.core.management import BaseCommand
from spotipy.oauth2 import SpotifyClientCredentials

from demo.models import Artist, Release, ReleaseTrack, Track


def _get_release_date(release):
    # Spotify doesn't like to guess, but I do.
    release_date = release["release_date"]
    release_date_precision = release["release_date_precision"]
    if release_date_precision == "day":
        # We're all good.
        pass
    elif release_date_precision == "month":
        release_date = f"{release_date}-01"
    elif release_date_precision == "year":
        release_date = f"{release_date}-01-01"
    else:
        raise ValueError(f"Unhandled release date precision: {release_date_precision}")
    return datetime.date.fromisoformat(release_date)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("artist_ids", nargs="+", type=str)

    def handle(self, *args, **options):
        counter = collections.Counter()

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        for artist in spotify.artists(options["artist_ids"])["artists"]:
            artist, created = Artist.objects.get_or_create(
                id=artist["id"], defaults={"name": artist["name"]}
            )
            if created:
                counter["artists"] += 1
            release_objs = [
                Release(
                    id=release["id"],
                    artist=artist,
                    title=release["name"],
                    release_date=_get_release_date(release),
                    type=release["album_type"],
                )
                for release in spotify.artist_albums(
                    artist.id, album_type="album,compilation,single"
                )["items"]
            ]
            releases = Release.objects.bulk_create(release_objs, ignore_conflicts=True)
            counter["releases"] += len(releases)

            # Things start to get funky when we look at tracks.
            # Tracks can:
            # - Have multiple artists.
            # - Appear on multiple releases.
            # - Have artist(s) different from the album artist
            #   (Various Artists compilations, Back To Mine albums, etc.).
            # We'll try to handle these cases as best we can.
            for release in releases:
                tracks = spotify.album_tracks(release.id)["items"]
                for track in tracks:
                    # We may not have every artist, so let's make sure.
                    artist_objs = []
                    for artist in track["artists"]:
                        artist_obj, created = Artist.objects.get_or_create(
                            id=artist["id"], defaults={"name": artist["name"]}
                        )
                        artist_objs.append(artist_obj)
                        if created:
                            counter["artists"] += 1

                    track_obj, created = Track.objects.get_or_create(
                        id=track["id"], defaults={"title": track["name"]}
                    )
                    if created:
                        counter["tracks"] += 1
                    track_obj.artists.set(artist_objs)

                    _, created = ReleaseTrack.objects.get_or_create(
                        release=release,
                        track=track_obj,
                        track_number=track["track_number"],
                    )
                    if created:
                        counter["release_tracks"] += 1

        self.stdout.write(pprint.pformat(counter))
