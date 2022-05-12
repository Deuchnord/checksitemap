#!/usr/bin/env python3

from xml.etree import ElementTree

from .fetcher import get_sitemap
from .exception import SitemapNotFoundError
from .utils import stderr, ERROR
from .sitemap import check_sitemap


def validate_sitemap(path: str) -> bool:
    xml = ElementTree.fromstring(get_sitemap(path))
    sitemap_valid, n_urls, n_passed = check_sitemap(xml)

    if not sitemap_valid:
        print()

    print(f"{n_passed} of {n_urls} URLs ({int(n_passed / n_urls * 100)}%) passed.")

    return sitemap_valid
