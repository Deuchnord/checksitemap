# checksitemap -- A tool to verify your sitemaps

checksitemap is a very simple tool that allows you to check the sitemaps of your websites.
Its development is not complete, but it is still currently usable.

## How to use it

First, install Python 3 and the `checksitemap` package from PyPI:

```bash
pip install checksitemap
```

You can now use tool, by invoking the command:

```bash
python checksitemap "https://example.com/sitemap.xml"
```

It will then check all the URLs in your sitemap and show errors if:

- the XML is malformed
- it references URLs that don't work correctly (i.e. they don't return 200-ish status codes)
- it references URLs that won't be indexable
- the priority or the change frequency are not valid
