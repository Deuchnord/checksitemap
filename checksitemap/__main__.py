#!/usr/bin/env python3

from . import ERROR, get_sitemap, stderr, check_sitemap

from argparse import ArgumentParser
from requests import ConnectionError
from requests.exceptions import HTTPError


def process_sitemap(url: str) -> int:
    try:
        sitemap = get_sitemap(url)
    except ConnectionError:
        stderr("The given URL was unreachable. Please double-check it.", ERROR)
        return 1
    except HTTPError:
        stderr("could not find the sitemap.", ERROR)
        return 1

    sitemap_valid, n_urls, n_passed = check_sitemap(sitemap)

    if not sitemap_valid:
        print()

    print(
        "%d of %d URLs (%d%%) passed."
        % (n_passed, n_urls, int(n_passed / n_urls * 100))
    )

    return 0 if sitemap_valid else 1


def main():
    try:
        args = ArgumentParser(description="Validate a sitemap.")

        args.add_argument("sitemap_location", type=str, help="the URL to the sitemap")

        args = args.parse_args()

        exit(process_sitemap(args.sitemap_location))
    except KeyboardInterrupt:
        exit(-1)
