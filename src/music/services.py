from music import models


class ImportArtistImages(object):
    def from_crawler_result(self, artist_images: list[dict[str, str]]):
        artist_images = list(filter(lambda ai: ai['image'] is not None, artist_images))
        if not artist_images:
            return

        # Get Artist objects from DB
        names = list(map(lambda r: r['name'], artist_images))
        artists = {a.name: a for a in models.Artist.objects.filter(name__in=names, image__isnull=True)}
        #  Discard results not exists
        names = artists.keys()
        artist_images = filter(lambda e: e['name'] in names, artist_images)
        if not artist_images:
            return

        # Process images
        images = []
        for entry in artist_images:
            artist = artists[entry['name']]
            image = self.process_image(artist, entry['image'])
            images.append(image)
        artists = artists.values()

        # SQLite backend does not respond with the generated IDs so bulk_create does not work as expected
        # models.ArtistImage.objects.bulk_create(images)
        for image in images:
            image.save()
            image.artist.image_id = image.id

        models.Artist.objects.bulk_update(artists, ['image'])

    def process_image(self, artist: models.Artist, url: str) -> models.ArtistImage:
        # Do (or queue) additional tasks like image download, etc
        image = models.ArtistImage(artist=artist, filename=url)
        artist.image = image
        return image
