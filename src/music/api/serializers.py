from rest_framework import serializers

from music import models


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ('id', 'name')


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ('id', 'name')


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = models.Album
        fields = ('id', 'title', 'tracks')
