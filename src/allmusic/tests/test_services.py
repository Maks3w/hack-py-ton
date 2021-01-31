import os
from unittest import TestCase, mock

from factory.fuzzy import FuzzyText

from allmusic import services, crawler

dir_path = os.path.dirname(os.path.realpath(__file__))


class ExtractImagesFromResponseTest(TestCase):
    def test_extract_images(self):
        with open(f'{dir_path}/fixtures/artists_result.html', mode='r') as f:
            response = f.read()

        result = services.extract_images_from_response(response)

        self.assertEqual(
            [
                {
                    'name': 'DJs@Work',
                    'image': None,
                },
                {
                    'name': 'The Icicle Works',
                    'image': 'https://rovimusic.rovicorp.com/image.jpg?c=hi3tC3A057LovoZr0ygyMz6KsMttLlyBmmVTZ6_CLs0=&f=2',
                },
            ],
            result,
        )


class AllmusicScrapperTest(TestCase):
    def test_look_for_artist(self):
        allmusic = services.AllmusicScrapper()
        artist_name = FuzzyText().fuzz()
        response = FuzzyText().fuzz()
        expected_result = [FuzzyText().fuzz()]

        with mock.patch.object(crawler.Crawler, 'request', return_value=response) as mock_request, \
                mock.patch.object(services, 'extract_images_from_response', return_value=expected_result) as mock_parse:
            result = allmusic.look_for_artist(artist_name)
            mock_request.assert_called_once_with(f'https://www.allmusic.com/search/artists/{artist_name}')
            mock_parse.assert_called_once_with(response)

        self.assertEqual(expected_result, result)
