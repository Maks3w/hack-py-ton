from unittest import mock

import celery
from django.test import TestCase

from music import services, models
from music.tests import factories


class ImportArtistImagesTest(TestCase):
    def test_no_results_from_db(self):
        artist_images = [
            {
                'name': 'NotExists',
                'image': 'NotExistsPhoto',
            },
        ]

        import_tool = services.ImportArtistImages()

        import_tool.from_crawler_result(artist_images)

        self.assertFalse(models.Artist.objects.exists())
        self.assertFalse(models.ArtistImage.objects.exists())

    def test_no_results_from_crawler(self):
        factories.ArtistFactory(name='artist without image', image=None),
        artist_images = [
            {
                'name': 'another artists without image',
                'image': None,
            },
        ]

        import_tool = services.ImportArtistImages()

        import_tool.from_crawler_result(artist_images)

        self.assertFalse(models.Artist.objects.filter(name='another artists without image').exists())
        self.assertFalse(models.ArtistImage.objects.exists())

    def test_from_crawler_result(self):
        artists = [
            factories.ArtistFactory(name='artist without image', image=None),
            factories.ArtistFactory(name='artist with image', image__filename='dont_replace_me'),
            factories.ArtistFactory(name='another artists without image', image=None),
        ]

        artist_images = [
            {
                'name': 'NotExists',
                'image': 'NotExistsPhoto',
            },
            {
                'name': 'another artists without image',
                'image': None,
            },
            {
                'name': 'artist without image',
                'image': 'NewImageSet',
            },
            {
                'name': 'artist with image',
                'image': 'error_image_replaced',
            },
        ]

        import_tool = services.ImportArtistImages()

        with mock.patch.object(celery.group, 'apply_async') as mock_group:
            import_tool.from_crawler_result(artist_images)
        self.assertEqual(mock_group.call_count, 1)

        artist_qs = models.Artist.objects
        artist_image_qs = models.ArtistImage.objects
        self.assertFalse(artist_qs.filter(name='NotExists').exists())
        self.assertFalse(artist_image_qs.filter(filename='NotExistsPhoto').exists())

        self.assertTrue(artist_qs.filter(name='artist with image', image__filename='dont_replace_me').exists())

        self.assertTrue(artist_qs.filter(name='another artists without image', image__isnull=True).exists())

        self.assertTrue(artist_qs.filter(name='artist without image', image__filename='NewImageSet').exists())
