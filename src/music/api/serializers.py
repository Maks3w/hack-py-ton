from rest_framework import serializers

from music import models


class ArtistSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.filename', default=None)

    class Meta:
        model = models.Artist
        fields = ('id', 'name', 'image')


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ('id', 'name')


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
