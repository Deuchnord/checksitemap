#!/usr/bin/env python3

from .utils import stderr, ERROR
from .exception import UrlError
from .fetcher import validate_url

XML_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
XML_ETREE_NAMESPACE = "{%s}" % XML_NAMESPACE

VALID_CHANGE_FREQS = [
    "always",
    "hourly",
    "daily",
    "weekly",
    "monthly",
    "yearly",
    "never",
]


def check_sitemap(sitemap) -> (bool, int, int):
    sitemap_valid = True
    n_urls = 0
    n_passed = 0

    if not sitemap.tag.startswith(XML_ETREE_NAMESPACE):
        stderr(
            f'missing XML namespace on <urlset> tag: add the xmlns="{XML_NAMESPACE}" attribute.'
        )
        sitemap_valid = False

    for item in sitemap:
        n_urls += 1

        if item.tag.replace(XML_ETREE_NAMESPACE, "") != "url":
            stderr(
                "invalid tag <%s>, expected <url>"
                % item.tag.replace(XML_ETREE_NAMESPACE, ""),
                ERROR,
            )
            continue

        if is_url_correct(item, n_urls):
            n_passed += 1
        elif sitemap_valid:
            sitemap_valid = False

    return sitemap_valid, n_urls, n_passed


def is_url_correct(url, n_url: int) -> bool:
    valid = True
    has_loc = False

    for prop in url:
        tag_name = prop.tag.replace(XML_ETREE_NAMESPACE, "")

        if tag_name not in ["loc", "lastmod", "changefreq", "priority"]:
            stderr("invalid <%s> tag for URL n°%d!" % (tag_name, n_url), ERROR)

            return False

        if tag_name == "loc":
            has_loc = True
            loc = prop.text
            try:
                validate_url(loc)
            except UrlError as e:
                valid = False
                stderr(e.msg, ERROR)

        if tag_name == "priority":
            priority = float(prop.text)

            if not 0 <= priority <= 1:
                stderr(
                    'invalid value "%s" for <%s> tag, must be a number between 0 and 1'
                    % (prop.text, tag_name),
                )
                valid = False

        if tag_name == "changefreq" and prop.text not in VALID_CHANGE_FREQS:
            stderr(
                "invalid value for <%s> tag, must be one of the following values: %s"
                % (tag_name, ", ".join(VALID_CHANGE_FREQS))
            )
            valid = False

    if not has_loc:
        stderr("URL n°%d has no mandatory <loc> tag!" % n_url, ERROR)
        return False

    return valid
