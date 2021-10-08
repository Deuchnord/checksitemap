#!/usr/bin/env python3

import sys
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET


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

    for item in sitemap:
        n_urls += 1

        if item.tag != '{http://www.sitemaps.org/schemas/sitemap/0.9}url':
            print('Error: invalid tag %s, expected <url>' % item.tag)
            continue

        location = item.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')

        if location is None:
            print("Error: missing mandatory <loc> tag for URL number %d!" % n_urls)
            continue

        r = requests.get(location.text)
        if r.status_code >= 300:
            print('Location "%s" returned %d status code' % (location.text, r.status_code))
            continue

        n_passed += 1

    return n_urls, n_passed


if __name__ == "__main__":
    exit(main(sys.argv[1]))

