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
    track_longest = serializers.IntegerField()
    track_shortest = serializers.IntegerField()
    milliseconds = serializers.IntegerField()

    class Meta:
        model = models.Album
        fields = ('id', 'title', 'tracks', 'track_longest', 'track_shortest', 'milliseconds')
