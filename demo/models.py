from django.db import models


class ReleaseType(models.TextChoices):
    ALBUM = "album"
    COMPILATION = "compilation"
    SINGLE_OR_EP = "single"


class Artist(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Release(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="releases", null=True
    )
    type = models.CharField(max_length=255, choices=ReleaseType.choices)
    title = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.artist.name} - {self.title}"


class Track(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    artists = models.ManyToManyField(Artist, related_name="tracks")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ReleaseTrack(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["release", "track_number"]

    def __str__(self):
        return f"[{self.release.artist.name} - {self.release.title}] {self.track_number}: {self.track.title}"
