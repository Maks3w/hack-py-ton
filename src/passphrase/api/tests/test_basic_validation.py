from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class BasicValidationViewTest(APITestCase):
    @parameterized.expand((
        # Passphrases, valid_count
        ([
        ], 0),
        ([
            'aa bb cc dd ee',  # Valid
            'aa bb cc dd aa',  # Invalid
            'aa bb cc dd aaa',  # Valid
        ], 2),
    ))
    def test_empty_list(self, passphrases: list, valid_count: int):
        r_retrieve = self.client.post(
            reverse('passphrase_api:basic_validation'),
            {'passphrases': '\n'.join(passphrases)},
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(valid_count, r_retrieve.data['valid'], r_retrieve.content)
