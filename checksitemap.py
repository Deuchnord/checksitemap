#!/usr/bin/env python3

from argparse import ArgumentParser
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET

XML_NAMESPACE = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XML_ETREE_NAMESPACE = '{%s}' % XML_NAMESPACE


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
        if prop.tag.replace(XML_ETREE_NAMESPACE, '') not in ['loc', 'lastmod', 'changefreq', 'priority']:
            print('Error: invalid <%s> tag for URL n°%d!' % (prop.tag.replace(XML_ETREE_NAMESPACE, ''), n_url))

            return False

        if prop.tag.replace(XML_ETREE_NAMESPACE, '') == 'loc':
            has_loc = True
            loc = prop.text
            r = requests.get(loc)
            if r.status_code >= 300:
                print('Location "%s" returned %d status code' % (loc, r.status_code))
                valid = False

    if not has_loc:
        print('Error: URL n°%d has no mandatory <loc> tag!' % n_url)
        return False

    return valid


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

