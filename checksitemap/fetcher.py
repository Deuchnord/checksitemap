#!/usr/bin/env python3

from typing import Union
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import time
import re
import requests

from .utils import stderr, NOTICE
from .exception import SitemapNotFoundError, UrlError

HTTPS_SCHEME = "https"
HTTP_SCHEME = "http"


def get_sitemap(place: str) -> str:
    try:
        tree = fetch_from_web(place)

        if tree:
            return tree

        with open(place) as file:
            return file.read()

    except FileNotFoundError as e:
        raise SitemapNotFoundError(f"file not found: {place}") from e
    except requests.exceptions.ConnectionError as e:
        raise SitemapNotFoundError(f"resource not found at {place}.") from e


def fetch_from_web(place: str) -> Union[None, str]:
    if not re.match(r"^https?://", place):
        return None

    parsed = urlparse(place)
    is_unsecured = False

    response = None
    if parsed.scheme == HTTP_SCHEME:
        try:
            response = requests.get(
                place.replace(f"{HTTP_SCHEME}://", f"{HTTPS_SCHEME}://"),
                allow_redirects=False,
            )
            stderr("upgraded to HTTPS automatically.", NOTICE)
        except requests.exceptions.ConnectionError:
            is_unsecured = True

    if response is None:
        response = requests.get(place, allow_redirects=False)

    if response.headers["content-type"].split(";")[0] != "text/xml":
        place = "%s://%s/sitemap.xml" % (parsed.scheme, parsed.netloc)
        response = requests.get(place)

    response.raise_for_status()

    if is_unsecured:
        stderr(
            "URL is not secured with HTTPS. You should consider upgrading to improve the security of your "
            "visitors."
        )

    return response.text


def validate_url(url: str, retries: int = 0) -> bool:
    r = requests.get(url, allow_redirects=False)

    try:
        r.raise_for_status()
        if r.status_code >= 300:
            stderr(
                'location "%s" redirects to "%s" with %d status code. You may want to remove it from your sitemap.'
                % (url, r.headers.get("Location"), r.status_code),
                NOTICE,
            )

    except requests.HTTPError as e:
        raise UrlError(
            f'location "{url}" returns an HTTP {e.response.status_code} status code.'
        )

    except requests.exceptions.ChunkedEncodingError:
        if retries == 5:
            raise UrlError(f'could not reach "{url}" because of a network error.')

        time_wait = 2**retries
        stderr(
            f'network error while checking "{url}", waiting for {time_wait} seconds.'
        )
        time.sleep(time_wait)

        return validate_url(url, retries + 1)

    return is_indexable(r)


def is_indexable(response: requests.Response) -> bool:
    url = response.url

    if "noindex" in response.headers.get("X-Robots-Tag", "").split(" "):
        stderr('location "%s" is not indexable based on X-Robots-Tag HTTP header' % url)
        return False

    html = BeautifulSoup(response.text, "html.parser")
    head = html.head

    if head is None:
        # this may happen sometimes, e.g. some redirection pages.
        # even though this is quite ugly, it remains valid HTML
        return True

    for meta in head.find_all("meta"):
        if meta.get("name") == "robots" and "noindex" in meta.get("content", "").split(
            ","
        ):
            stderr(
                'location "%s" is not indexable based on <meta name="robots" /> HTML tag'
                % url
            )
            return False

    return True
