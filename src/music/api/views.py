from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from music import models
from music.api import serializers


class ArtistViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer
