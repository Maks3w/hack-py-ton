import base64
import random

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from music import models
from music.tests import factories


def authentication():
    data = 'root:root'
    credentials = base64.b64encode(data.encode("utf-8")).strip()
    auth_string = f'Basic {credentials.decode("utf-8")}'
    return {'HTTP_AUTHORIZATION': auth_string}


class AlbumViewTest(APITestCase):
    fixtures = [
        'core/fixtures/users.json',
    ]

    def test_anonymous_forbidden(self):
        r_retrieve = self.client.get(reverse('music_api:album-list'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r_retrieve.status_code, r_retrieve.content)

    def test_empty_list(self):
        r_retrieve = self.client.get(reverse('music_api:album-list'), format='json', **authentication())
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(0, r_retrieve.data['count'], r_retrieve.content)

    def test_list(self):
        track = factories.TrackFactory.create()
        albums = [track.album]

        r_retrieve = self.client.get(reverse('music_api:album-list'), format='json', **authentication())
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(len(albums), r_retrieve.data['count'], r_retrieve.content)

        self.assert_serialization_match(albums[0], r_retrieve.data['results'][0])

    def test_list_filter_by_artist(self):
        albums = factories.AlbumFactory.create_batch(2)
        target_album = random.choice(albums)

        r_retrieve = self.client.get(
            reverse('music_api:album-list'),
            {'artist_id': target_album.artist_id},
            format='json',
            **authentication(),
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(1, r_retrieve.data['count'], r_retrieve.content)

        self.assert_serialization_match(target_album, r_retrieve.data['results'][0])

    def assert_serialization_match(self, album: models.Album, result: dict):
        self.assertEqual(album.id, result['id'], result)
        self.assertEqual(album.title, result['title'], result)
        self.assertIn('artist', result, result)
        self.assertEqual(album.artist.name, result['artist']['name'], result['artist'])
        self.assertEqual(album.artist.image.filename, result['artist']['image'], result['artist'])
