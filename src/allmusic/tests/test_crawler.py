import responses
from django.test import TestCase
from factory.fuzzy import FuzzyText
from faker import Faker

from allmusic import crawler


class CrawlerTest(TestCase):
    def test_request_ok(self):
        url = Faker().uri()
        response = FuzzyText().fuzz()

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                url,
                body=response,
            )

            result = crawler.Crawler.request(url)

        self.assertEqual(response, result)

    def test_request_binary(self):
        url = Faker().uri()
        response = Faker().binary()

        with responses.RequestsMock() as rsps, \
                self.assertRaisesRegex(ValueError, 'Not HTML response'):
            rsps.add(
                responses.GET,
                url,
                body=response,
            )

            crawler.Crawler.request(url)
