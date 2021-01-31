from lxml import html, etree

from allmusic.crawler import Crawler


def extract_images_from_response(response: str) -> list[dict[str, str]]:
    root = html.fromstring(response)
    results = []
    artists = root.xpath(f'.//li[@class="artist"]')
    for artist in artists:
        artist = etree.XPathEvaluator(artist)
        name = artist('string(.//div[@class="name"]//a/text())')
        photo = artist('string(.//div[@class="photo"]//img/@src)')
        results.append(
            {
                'name': name,
                'image': photo if photo != '' else None,
            },
        )
    return results


class AllmusicScrapper(object):
    ARTIST_SEARCH_URL_TEMPLATE = 'https://www.allmusic.com/search/artists/{name}'
    ARTIST_SEARCH_URL_PAGINATION_TEMPLATE = 'https://www.allmusic.com/search/artists/{name}/all/{page}'

    def __init__(self):
        self.crawler = Crawler()

    def look_for_artist(self, name: str) -> list[dict[str, str]]:
        """
        It returns a list of structures similar to
        ```
        [
            {
                'name': 'DJs@Work',
                'photo': None,
            },
            {
                'name': 'The Icicle Works',
                'photo': 'https://rovimusic.rovicorp.com/image.jpg?c=hi3tC3A057LovoZr0ygyMz6KsMttLlyBmmVTZ6_CLs0=&f=2',
            },
        ]
        ```
        """
        url = self.ARTIST_SEARCH_URL_TEMPLATE.format(name=name)

        response = self.crawler.request(url)

        return extract_images_from_response(response)
