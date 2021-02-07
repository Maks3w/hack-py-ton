from django.db.models import QuerySet
from rest_framework import serializers

from music import models


def add_relation_prefix(prefix: str, relations: list[str]) -> list[str]:
    return [f'{prefix}__{r}' for r in relations]


class ArtistSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.filename', default=None)

    class Meta:
        model = models.Artist
        fields = ('id', 'name', 'image')

    @staticmethod
    def build_queryset(qs: QuerySet) -> QuerySet:
        return qs \
            .prefetch_related(*ArtistSerializer.prefetch_optimizations()) \
            .select_related(*ArtistSerializer.select_optimizations())

    @staticmethod
    def prefetch_optimizations():
        return []

    @staticmethod
    def select_optimizations():
        return ['image']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ('id', 'name')

    @staticmethod
    def optimize_queryset(qs: QuerySet) -> QuerySet:
        return qs

    @staticmethod
    def prefetch_optimizations():
        return []

    @staticmethod
    def select_optimizations():
        return []


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)
    artist = ArtistSerializer()
    track_count = serializers.IntegerField()
    track_longest = serializers.IntegerField()
    track_shortest = serializers.IntegerField()
    milliseconds = serializers.IntegerField()

    class Meta:
        model = models.Album
        fields = (
            'id', 'title', 'tracks', 'artist', 'track_count', 'track_longest', 'track_shortest', 'milliseconds',
        )

    @staticmethod
    def build_queryset(qs: QuerySet) -> QuerySet:
        return qs \
            .prefetch_related('tracks', *AlbumSerializer.prefetch_optimizations()) \
            .select_related('artist', *AlbumSerializer.select_optimizations()) \
            .with_track_count() \
            .with_track_longest() \
            .with_track_shortest() \
            .with_milliseconds()

    @staticmethod
    def prefetch_optimizations():
        return add_relation_prefix('artist', ArtistSerializer.prefetch_optimizations()) + \
               add_relation_prefix('tracks', TrackSerializer.prefetch_optimizations()) + \
               []

    @staticmethod
    def select_optimizations():
        return add_relation_prefix('artist', ArtistSerializer.select_optimizations()) + \
               add_relation_prefix('tracks', TrackSerializer.select_optimizations()) + \
               []
