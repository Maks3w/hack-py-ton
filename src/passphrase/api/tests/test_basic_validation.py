from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from passphrase.api.tests.mixins import AbstractValidationViewSetTestCase


def passphrase_dataset():
    return (
        # Passphrases, valid_count
        ([
            'aa bb cc dd ee',  # Valid
            'aa bb cc dd aa',  # Invalid
            'aa bb cc dd aaa',  # Valid
        ], 2),
    )


class BasicValidationViewTest(AbstractValidationViewSetTestCase, APITestCase):
    def get_path(self) -> str:
        return reverse('passphrase_api:basic_validation-list')

    @parameterized.expand((passphrase_dataset()))
    def test_validation(self, passphrases: list, valid_count: int):
        r_retrieve = self.client.post(
            self.get_path(),
            {'passphrases': '\n'.join(passphrases)},
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(valid_count, r_retrieve.data['valid'], r_retrieve.content)

    @parameterized.expand((passphrase_dataset()))
    def test_validation_crlf(self, passphrases: list, valid_count: int):
        r_retrieve = self.client.post(
            self.get_path(),
            {'passphrases': '\r\n'.join(passphrases)},
        )
        self.assertEqual(status.HTTP_200_OK, r_retrieve.status_code, r_retrieve.content)

        self.assertEqual(valid_count, r_retrieve.data['valid'], r_retrieve.content)
