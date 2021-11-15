# checksitemap -- A tool to verify your sitemaps

[![Coverage Status](https://coveralls.io/repos/github/Deuchnord/checksitemap/badge.svg?branch=main)](https://coveralls.io/github/Deuchnord/Aurornis?branch=main)

checksitemap is a very simple tool that allows you to check the sitemaps of your websites.
Its development is not complete, but it is still currently usable.

## How to use it

First, install Python 3 and the `checksitemap` package from PyPI:

```bash
pip install checksitemap
```

You can now use invoke the command:

```bash
checksitemap "https://example.com/sitemap.xml"
```

If you prefer, you can also use `checksitemap` on a local file:

```bash
checksitemap path/to/local/file.xml
```

It will then check all the URLs in your sitemap and show errors if:

- the XML is malformed
- it references URLs that don't work correctly (i.e. they don't return 200-ish status codes)
- it references URLs that won't be indexable
- the priority or the change frequency are not valid
