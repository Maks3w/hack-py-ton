from unittest import TestCase

from parameterized import parameterized

from passphrase import services


class BasicValidation(TestCase):
    @parameterized.expand((
        # passphrase, Valid
        ('aa bb cc dd ee', True),
        ('aa bb cc dd aa', False),
        ('aa bb cc dd aaa', True),
    ))
    def test_basic_validation(self, passphrase: str, valid: bool):
        self.assertEqual(valid, services.basic_validation(passphrase), passphrase)
