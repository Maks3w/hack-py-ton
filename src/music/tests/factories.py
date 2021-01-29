import factory
from factory.fuzzy import FuzzyText

from music import models


class ArtistFactory(factory.django.DjangoModelFactory):
    name = FuzzyText()

    class Meta:
        model = models.Artist
