#!/usr/bin/env python3

from aurornis import run


def run_cmd(xml: str):
    return run(["checksitemap", xml])


def test_check_valid_sitemap_from_local_file():
    result = run_cmd("test_assets/valid_sitemap.xml")
    assert result.successful
    assert result.stderr == ""
    assert result.stdout == "3 of 3 URLs (100%) passed.\n"


def test_check_invalid_sitemap_from_local_file_missing_namespace():
    result = run_cmd(f"test_assets/invalid_sitemap_missing_namespace.xml")
    assert not result.successful
    assert (
        result.stderr == "Warning: missing XML namespace on <urlset> tag: "
        'add the xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" attribute.\n'
    )
    assert result.stdout == "\n3 of 3 URLs (100%) passed.\n"


def test_check_invalid_sitemap_from_local_file_invalid_tag():
    result = run_cmd(f"test_assets/invalid_sitemap_invalid_tag.xml")
    assert not result.successful
    assert result.stderr == "Error: invalid <is_a_cool_page> tag for URL n°1!\n"
    assert result.stdout == "\n2 of 3 URLs (66%) passed.\n"


def test_check_invalid_sitemap_from_local_file_missing_loc():
    result = run_cmd(f"test_assets/invalid_sitemap_missing_loc.xml")
    assert not result.successful
    assert result.stderr == "Error: URL n°1 has no mandatory <loc> tag!\n"
    assert result.stdout == "\n2 of 3 URLs (66%) passed.\n"


def test_check_invalid_sitemap_from_local_file_invalid_priority():
    result = run_cmd(f"test_assets/invalid_sitemap_invalid_priority.xml")
    assert not result.successful
    assert (
        result.stderr
        == 'Warning: invalid value "42" for <priority> tag, must be a number between 0 and 1\n'
    )
    assert result.stdout == "\n2 of 3 URLs (66%) passed.\n"


def test_check_invalid_sitemap_from_local_file_changefreq():
    result = run_cmd(f"test_assets/invalid_sitemap_changefreq.xml")
    assert not result.successful
    assert (
        result.stderr
        == "Warning: invalid value for <changefreq> tag, must be one of the following values: "
        "always, hourly, daily, weekly, monthly, yearly, never\n"
    )
    assert result.stdout == "\n2 of 3 URLs (66%) passed.\n"


def test_check_sitemap_containing_404_error_from_local_file():
    result = run_cmd("test_assets/sitemap_with_404.xml")
    assert not result.successful
    assert (
        result.stderr
        == 'Error: location "https://deuchnord.fr/blog/foo" returns an HTTP 404 status code.\n'
    )
    assert result.stdout == "\n3 of 4 URLs (75%) passed.\n"


def test_check_sitemap_on_non_existing_site():
    result = run_cmd("https://thissitedoesnotexist.dns")
    assert not result.successful
    assert (
        result.stderr
        == "Error: resource not found at https://thissitedoesnotexist.dns.\n"
    )
