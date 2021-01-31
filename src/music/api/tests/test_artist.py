from random import randint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from music import models
from music.tests import factories


class ArtistViewTest(APITestCase):
    def test_empty_list(self):
        r_retrieve = self.client.get(reverse('music_api:artist-list'), format='json')
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(0, r_retrieve.data['count'], r_retrieve.content)

    def test_list(self):
        artists = factories.ArtistFactory.create_batch(randint(1, 20))

        r_retrieve = self.client.get(reverse('music_api:artist-list'), format='json')
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(len(artists), r_retrieve.data['count'], r_retrieve.content)

        self.assert_serialization_match(artists[0], r_retrieve.data['results'][0])

    def assert_serialization_match(self, artist: models.Artist, result: dict):
        self.assertEqual(artist.id, result['id'], result)
        self.assertEqual(artist.name, result['name'], result)
        self.assertEqual(artist.image.filename, result['image'], result)
