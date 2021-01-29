from random import randint

from django.test import TestCase

from music import models
from music.tests import factories


class AlbumTest(TestCase):
    def test_with_artist_name(self):
        album = factories.AlbumFactory.create()
        album = models.Album.objects.with_artist_name().get(id=album.id)

        self.assertEqual(album.artist.name, album.artist_name)

    def test_with_track_count(self):
        album = factories.AlbumFactory.create()
        factories.TrackFactory.create_batch(album=album, size=randint(1, 20))

        album = models.Album.objects.with_track_count().get(id=album.id)

        self.assertEqual(album.tracks.count(), album.track_count)

    def test_with_track_longest(self):
        album = factories.AlbumFactory.create()
        shortest_track = factories.TrackFactory(album=album, milliseconds=1)
        longest_track = factories.TrackFactory(album=album, milliseconds=2)

        album = models.Album.objects.with_track_longest().get(id=album.id)

        self.assertEqual(longest_track.milliseconds, album.track_longest)
        self.assertNotEqual(shortest_track.milliseconds, album.track_longest)

    def test_with_track_shortest(self):
        album = factories.AlbumFactory.create()
        shortest_track = factories.TrackFactory(album=album, milliseconds=1)
        longest_track = factories.TrackFactory(album=album, milliseconds=2)

        album = models.Album.objects.with_track_shortest().get(id=album.id)

        self.assertEqual(shortest_track.milliseconds, album.track_shortest)
        self.assertNotEqual(longest_track.milliseconds, album.track_shortest)

    def test_with_milliseconds(self):
        album = factories.AlbumFactory.create()
        shortest_track = factories.TrackFactory(album=album, milliseconds=1)
        longest_track = factories.TrackFactory(album=album, milliseconds=2)
        milliseconds = sum(map(lambda t: t.milliseconds, [shortest_track, longest_track]))

        album = models.Album.objects.with_milliseconds().get(id=album.id)

        self.assertEqual(milliseconds, album.milliseconds)
