from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from passphrase.api.tests.mixins import AbstractValidationViewSetTestCase


class AdvancedValidationViewTest(AbstractValidationViewSetTestCase, APITestCase):
    def get_path(self) -> str:
        return reverse('passphrase_api:advanced_validation-list')

    @parameterized.expand((
        # Passphrases, valid_count
        ([
            'abcde fghij',  # Valid
            'abcde xyz ecdab',  # Invalid
            'a ab abc abd abf abj',  # Valid
        ], 2),
    ))
    def test_validation(self, passphrases: list, valid_count: int):
        r_retrieve = self.client.post(
            self.get_path(),
            {'passphrases': '\n'.join(passphrases)},
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(valid_count, r_retrieve.data['valid'], r_retrieve.content)
