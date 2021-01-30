from abc import abstractmethod, ABCMeta

from parameterized import parameterized
from rest_framework import status


class AbstractValidationViewSetTestCase(metaclass=ABCMeta):
    @abstractmethod
    def get_path(self) -> str:
        raise NotImplementedError

    @parameterized.expand((
        # Data, Field, Error
        ({},                  'passphrases', 'This field is required.'),
        ({'passphrases': ''}, 'passphrases', 'This field may not be blank.'),
    ))
    def test_empty_request(self, data: dict, field: str, error: str):
        r_retrieve = self.client.post(self.get_path(), data)
        self.assertFieldError(r_retrieve, field, error)

    def assertFieldError(self, response, field: str, error: str):
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.content)
        self.assertIn(field, response.data)
        self.assertEqual(error, response.data[field][0])
