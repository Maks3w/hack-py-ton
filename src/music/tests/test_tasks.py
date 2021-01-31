from unittest import mock

import responses
from django.test import TestCase
from factory.fuzzy import FuzzyText

from music import tasks, services
from music.tests import factories


class ProcessImageTest(TestCase):
    def test_process_image(self):
        image = factories.ArtistImageFactory()

        with mock.patch.object(tasks, 'save_image') as mock_save_image:
            tasks.process_image(image.id)
            mock_save_image.assert_called_once_with(image)

    def test_save_image(self):
        image = factories.ArtistImageFactory()
        response = FuzzyText().fuzz()

        with responses.RequestsMock() as rsps, \
                mock.patch.object(services.ArtistImageSave, 'store_file') as mock_store_file:
            rsps.add(
                responses.GET,
                image.filename,
                body=response,
            )
            tasks.save_image(image)
            mock_store_file.assert_called_once_with(image, response.encode())
