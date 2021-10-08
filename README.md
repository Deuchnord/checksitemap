# checksitemap -- A tool to verify your sitemaps

checksitemap is a very simple tool that allows you to check the sitemaps of your websites.
Its development is not complete, but it is still currently usable.

## How to use it

All you need is Python 3 along with PIP and [the `requests` package](https://pypi.org/project/requests/).
To use this tool, just invoke the command like this:

```bash
python checksitemap "https://example.com/sitemap.xml"
```

It will then check all the URLs in your sitemap and tell you if it finds any broken link.

