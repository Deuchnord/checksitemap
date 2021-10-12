#!/usr/bin/env python3

from argparse import ArgumentParser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import requests
import xml.etree.ElementTree as ET

XML_NAMESPACE = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XML_ETREE_NAMESPACE = '{%s}' % XML_NAMESPACE
VALID_CHANGE_FREQS = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']


def main(url: str) -> int:
    xml = requests.get(url)

    if xml.headers['content-type'].split(';')[0] != 'text/xml':
        parsed = urlparse(url)
        url = '%s://%s/sitemap.xml' % (parsed.scheme, parsed.netloc)
        xml = requests.get(url)
        if xml.status_code == 200:
            print('Sitemap found at %s' % url)

    xml.raise_for_status()
    sitemap = ET.fromstring(xml.text)

    n_urls, n_passed = check_sitemap(sitemap)

    if n_passed != n_urls:
        print()

    print('%d of %d URLs (%d%%) passed.' % (n_passed, n_urls, int(n_passed / n_urls * 100)))

    return 0 if n_passed == n_urls else 1


def check_sitemap(sitemap) -> (int, int):
    n_urls = 0
    n_passed = 0

    if not sitemap.tag.startswith(XML_ETREE_NAMESPACE):
        print('Warning: missing XML namespace on <urlset> tag: please add xmlns="%s"' % XML_NAMESPACE)

    for item in sitemap:
        n_urls += 1

        if item.tag.replace(XML_ETREE_NAMESPACE, '') != 'url':
            print('Error: invalid tag <%s>, expected <url>' % item.tag.replace(XML_ETREE_NAMESPACE, ''))
            continue

        if is_url_correct(item, n_urls):
            n_passed += 1

    return n_urls, n_passed


def is_url_correct(url, n_url) -> bool:
    valid = True
    has_loc = False

    for prop in url:
        tag_name = prop.tag.replace(XML_ETREE_NAMESPACE, '')

        if tag_name not in ['loc', 'lastmod', 'changefreq', 'priority']:
            print('Error: invalid <%s> tag for URL n°%d!' % (tag_name, n_url))

            return False

        if tag_name == 'loc':
            has_loc = True
            loc = prop.text
            r = requests.get(loc)
            if r.status_code >= 300:
                print('Location "%s" returned %d status code' % (loc, r.status_code))
                valid = False

            valid = valid and is_indexable(loc, r)

        if tag_name == 'priority':
            try:
                priority = float(prop.text)

                if not 0 <= priority <= 1:
                    raise ValueError()

            except ValueError:
                print('Invalid value "%s" for <%s> tag, must be a number between 0 and 1' % (prop.text, tag_name))
                valid = False

        if tag_name == 'changefreq' and prop.text not in VALID_CHANGE_FREQS:
            print('Invalid vale for <%s> tag, must be one of the following values: %s' % (
                tag_name,
                ', '.join(VALID_CHANGE_FREQS)
            ))

    if not has_loc:
        print('Error: URL n°%d has no mandatory <loc> tag!' % n_url)
        return False

    return valid


def is_indexable(loc: str, response: requests.Response) -> bool:
    if "noindex" in response.headers.get("X-Robots-Tag", "").split(" "):
        print('Location "%s" is not indexable based on X-Robots-Tag HTTP header' % loc)
        return False

    html = BeautifulSoup(response.text, 'html.parser')
    for meta in html.head.find_all("meta"):
        if meta.get("name") == "robots" and "noindex" in meta.get("content", "").split(","):
            print('Location "%s" is not indexable based on <meta name="robots" /> HTML tag' % loc)
            return False

    return True


if __name__ == "__main__":
    try:
        args = ArgumentParser(
            description="Validate a sitemap."
        )

        args.add_argument("sitemap_location", type=str, help="the URL to the sitemap")

        args = args.parse_args()

        exit(main(args.sitemap_location))
    except KeyboardInterrupt:
        exit(-1)

