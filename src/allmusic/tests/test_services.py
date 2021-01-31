import os
from unittest import TestCase

from allmusic import services

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
                    'photo': None,
                },
                {
                    'name': 'The Icicle Works',
                    'photo': 'https://rovimusic.rovicorp.com/image.jpg?c=hi3tC3A057LovoZr0ygyMz6KsMttLlyBmmVTZ6_CLs0=&f=2',
                },
            ],
            result,
        )
