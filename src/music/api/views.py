from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from music import models
from music.api import serializers


class ArtistViewSet(ListModelMixin, GenericViewSet):
    queryset = serializers.ArtistSerializer.build_queryset(models.Artist.objects).all()
    serializer_class = serializers.ArtistSerializer


class AlbumViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        queryset = serializers.AlbumSerializer.build_queryset(models.Album.objects).all()
        artist_id = self.request.query_params.get('artist_id', None)
        if artist_id is not None:
            queryset = queryset.filter(artist_id=artist_id)
        return queryset
