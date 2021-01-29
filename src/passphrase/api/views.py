from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from passphrase import services


def create_response(valid: int) -> Response:
    return Response({'valid': valid}, status=status.HTTP_200_OK)


class BasicValidationView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        passphrases = request.data['passphrases'].split('\n')
        results = map(services.basic_validation, passphrases)
        valid = filter(lambda r: r, results)

        return create_response(len(list(valid)))


class AdvancedValidationView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        passphrases = request.data['passphrases'].split('\n')
        results = map(services.advanced_validation, passphrases)
        valid = filter(lambda r: r, results)

        return create_response(len(list(valid)))
