from unittest import TestCase

from parameterized import parameterized

from passphrase import services


class BasicValidation(TestCase):
    @parameterized.expand((
        # passphrase, Valid
        ('', False),
        (' ', False),
        ('aa bb cc dd ee', True),
        ('aa bb cc dd aa', False),
        ('aa bb cc dd aaa', True),
    ))
    def test_basic_validation(self, passphrase: str, valid: bool):
        self.assertEqual(valid, services.basic_validation(passphrase), passphrase)


class AdvancedValidation(TestCase):
    @parameterized.expand((
        # passphrase, Valid
        ('', False),
        (' ', False),
        ('abcde fghij', True),
        ('abcde xyz ecdab', False),
        ('a ab abc abd abf abj', True),
        ('iiii oiii ooii oooi oooo', True),
        ('oiii ioii iioi iiio', False),
    ))
    def test_advanced_validation(self, passphrase: str, valid: bool):
        self.assertEqual(valid, services.advanced_validation(passphrase), passphrase)
