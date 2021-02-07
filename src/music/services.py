from celery import group

from music import models, tasks


class ImportArtistImages(object):
    def from_crawler_result(self, artist_images: list[dict[str, str]]):
        artist_images = [ai for ai in artist_images if ai['image'] is not None]
        if not artist_images:
            return

        # Get Artist objects from DB
        names = [ai['name'] for ai in artist_images]
        artists = {a.name: a for a in models.Artist.objects.filter(name__in=names, image__isnull=True).all()}
        #  Discard results not exists
        names = artists.keys()
        artist_images = [ai for ai in artist_images if ai['name'] in names]
        if not artist_images:
            return

        # Process images
        images = []
        for entry in artist_images:
            artist = artists[entry['name']]
            artist.image = models.ArtistImage(artist=artist, filename=entry['image'])
            images.append(artist.image)
        artists = artists.values()

        # SQLite backend does not respond with the generated IDs so bulk_create does not work as expected
        # models.ArtistImage.objects.bulk_create(images)
        process_images = []
        for image in images:
            image.save()
            image.artist.image_id = image.id
            process_images.append(tasks.process_image.s(image.id))

        models.Artist.objects.bulk_update(artists, ['image'])
        group(tasks).apply_async()


class ArtistImageSave(object):
    def store_file(self, ai: models.ArtistImage, content: bytes):
        pass
