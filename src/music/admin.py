from django.contrib import admin

from music import models


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    autocomplete_fields = ('artist',)
    search_fields = ('title',)
    list_display = ('title',)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    autocomplete_fields = ('album',)
    search_fields = ('name',)
    list_display = ('name',)
