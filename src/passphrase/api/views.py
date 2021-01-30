from abc import ABCMeta, abstractmethod

from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from passphrase import services
from passphrase.api import serializers


class AbstractValidationViewSet(CreateModelMixin, GenericViewSet, metaclass=ABCMeta):
    @abstractmethod
    def get_validation_service(self) -> callable:
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        passphrases = serializer.save()['passphrases']
        results = map(self.get_validation_service(), passphrases)
        valid = filter(lambda r: r, results)

        return Response({'valid': len(list(valid))}, status=status.HTTP_200_OK)


class BasicValidationViewSet(AbstractValidationViewSet):
    serializer_class = serializers.PassphraseSerializer

    def get_validation_service(self) -> callable:
        return services.basic_validation


class AdvancedValidationViewSet(AbstractValidationViewSet):
    serializer_class = serializers.PassphraseSerializer

    def get_validation_service(self) -> callable:
        return services.advanced_validation
