from django.db import models


class Artist(models.Model):
    id = models.AutoField(db_column='ArtistId', primary_key=True)
    name = models.TextField(db_column='Name', blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        managed = True
        db_table = 'artists'


class Album(models.Model):
    id = models.AutoField(db_column='AlbumId', primary_key=True)
    title = models.TextField(db_column='Title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='ArtistId')

    def __str__(self):
        return f'{self.id} - {self.title}'

    class Meta:
        managed = True
        db_table = 'albums'


class Track(models.Model):
    id = models.AutoField(db_column='TrackId', primary_key=True)
    name = models.TextField(db_column='Name')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column='AlbumId')
    milliseconds = models.IntegerField(db_column='Milliseconds')

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        managed = True
        db_table = 'tracks'
