from django.db import models
from django.db.models import Min, Max, Sum, F, Count


class Artist(models.Model):
    id = models.AutoField(db_column='ArtistId', primary_key=True)
    name = models.TextField(db_column='Name', blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        managed = True
        db_table = 'artists'
        ordering = ['id']


class Album(models.Model):
    id = models.AutoField(db_column='AlbumId', primary_key=True)
    title = models.TextField(db_column='Title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', db_column='ArtistId')

    class QuerySet(models.QuerySet):
        @property
        def _aggregate_ordering_fix(self):
            """
            Annotations with Aggregations are not mark as ordered so may eventually raise warnings like
            UnorderedObjectListWarning.

            This function set an explicit order_by based on the Model.META.ordering value. If you don't like then call
            `order_by()` with your own arguments or with an empty for remove the effect

            https://docs.djangoproject.com/en/3.1/topics/db/aggregation/#interaction-with-default-ordering-or-order-by
            """
            return self.order_by(*self.model._meta.ordering)

        def with_artist_name(self):
            return self.annotate(artist_name=F('artist__name'))

        def with_track_count(self):
            return self._aggregate_ordering_fix.annotate(track_count=Count('tracks'))

        def with_track_longest(self):
            return self._aggregate_ordering_fix.annotate(track_longest=Max('tracks__milliseconds'))

        def with_track_shortest(self):
            return self._aggregate_ordering_fix.annotate(track_shortest=Min('tracks__milliseconds'))

        def with_milliseconds(self):
            return self._aggregate_ordering_fix.annotate(milliseconds=Sum('tracks__milliseconds'))

    objects = QuerySet.as_manager()

    def __str__(self):
        return f'{self.id} - {self.title}'

    class Meta:
        managed = True
        db_table = 'albums'
        ordering = ['id']


class Track(models.Model):
    id = models.AutoField(db_column='TrackId', primary_key=True)
    name = models.TextField(db_column='Name')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks', db_column='AlbumId')
    milliseconds = models.IntegerField(db_column='Milliseconds')

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        managed = True
        db_table = 'tracks'
        ordering = ['id']
