import factory
from factory.fuzzy import FuzzyText, FuzzyInteger

from music import models


class ArtistImageFactory(factory.django.DjangoModelFactory):
    filename = FuzzyText(length=128)

    class Meta:
        model = models.ArtistImage


class ArtistFactory(factory.django.DjangoModelFactory):
    name = FuzzyText()
    image = factory.SubFactory(ArtistImageFactory)

    class Meta:
        model = models.Artist


class AlbumFactory(factory.django.DjangoModelFactory):
    artist = factory.SubFactory(ArtistFactory)
    title = FuzzyText()

    class Meta:
        model = models.Album


class TrackFactory(factory.django.DjangoModelFactory):
    album = factory.SubFactory(AlbumFactory)
    name = FuzzyText()
    milliseconds = FuzzyInteger(1)

    class Meta:
        model = models.Track
