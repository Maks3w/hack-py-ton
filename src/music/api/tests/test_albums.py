import base64

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

    def assert_serialization_match(self, artist: models.Album, result: dict):
        self.assertEqual(artist.id, result['id'], result)
        self.assertEqual(artist.title, result['title'], result)
