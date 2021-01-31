import logging

import requests
from celery import current_app

from music import models, services

logger = logging.getLogger(__name__)


@current_app.task()
def process_image(artist_image: int):
    logger.info(f'Artist image ({artist_image})')
    ai = models.ArtistImage.objects.get(id=artist_image)
    save_image(ai)


def save_image(ai: models.ArtistImage):
    r = requests.get(ai.filename)
    saver = services.ArtistImageSave()
    saver.store_file(ai, r.content)
