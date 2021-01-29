from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class AdvancedValidationViewTest(APITestCase):
    @parameterized.expand((
        # Passphrases, valid_count
        ([
        ], 0),
        ([
            'abcde fghij',  # Valid
            'abcde xyz ecdab',  # Invalid
            'a ab abc abd abf abj',  # Valid
        ], 2),
    ))
    def test_empty_list(self, passphrases: list, valid_count: int):
        r_retrieve = self.client.post(
            reverse('passphrase_api:advanced_validation'),
            {'passphrases': '\n'.join(passphrases)},
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(valid_count, r_retrieve.data['valid'], r_retrieve.content)
