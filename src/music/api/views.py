from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from music import models
from music.api import serializers


class ArtistViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer


class AlbumViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
