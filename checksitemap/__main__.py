#!/usr/bin/env python3

from . import ERROR, stderr, validate_sitemap
from .exception import SitemapError

from argparse import ArgumentParser
import sys


def main():
    try:
        args = ArgumentParser(description="Validate a sitemap.")
        args.add_argument("sitemap_location", type=str, help="the URL to the sitemap")
        args = args.parse_args()

        sys.exit(0 if validate_sitemap(args.sitemap_location) else 1)
    except SitemapError as e:
        stderr(e.msg, ERROR)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(-1)
