from lxml import html


def extract_images_from_response(response: str) -> list[dict[str, str]]:
    root = html.fromstring(response)
    results = []
    artists = root.xpath(f'.//li[@class="artist"]')
    for artist in artists:
        name = next(iter(artist.xpath(f'.//div[@class="name"]//a/text()')), None)
        photo = next(iter(artist.xpath(f'.//div[@class="photo"]//img/@src')), None)
        results.append(
            {
                'name': name,
                'photo': photo,
            },
        )
    return results
