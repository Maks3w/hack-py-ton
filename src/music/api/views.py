from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from music import models
from music.api import serializers


class ArtistViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Artist.objects.select_related('image').all()
    serializer_class = serializers.ArtistSerializer


class AlbumViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        queryset = models.Album.objects \
            .prefetch_related('tracks') \
            .select_related('artist') \
            .select_related('artist__image') \
            .with_track_count() \
            .with_track_longest() \
            .with_track_shortest() \
            .with_milliseconds()
        artist_id = self.request.query_params.get('artist_id', None)
        if artist_id is not None:
            queryset = queryset.filter(artist_id=artist_id)
        return queryset
