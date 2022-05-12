#!/usr/bin/env python3


class SitemapError(RuntimeError):
    def __init__(self, msg: str):
        self.msg = msg


class SitemapNotFoundError(SitemapError):
    pass


class InvalidSitemapError(SitemapError):
    pass


class UrlError(IOError):
    def __init__(self, msg: str):
        self.msg = msg
