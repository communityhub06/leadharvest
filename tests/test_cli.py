import pytest

from leadharvest.cli import build_parser, collect_urls, harvest, parse_regions
from leadharvest.fetch import canonical_url, make_session


def test_canonical_url_adds_scheme_and_strips_fragment():
    assert canonical_url("acme.fr/about#team") == "https://acme.fr/about"
    assert canonical_url("  https://acme.fr  ") == "https://acme.fr"
    assert canonical_url("#top") is None
    assert canonical_url("ftp://acme.fr") is None


def test_collect_urls_from_file_dedupes(tmp_path):
    listing = tmp_path / "urls.txt"
    listing.write_text("# comment\nacme.fr\nhttps://acme.fr\n\nbroken one\n", encoding="utf-8")
    args = build_parser().parse_args(["-i", str(listing)])
    assert collect_urls(args, make_session()) == ["https://acme.fr", "https://broken one"]


def test_collect_urls_without_targets_is_empty():
    args = build_parser().parse_args([])
    assert collect_urls(args, make_session()) == []


def test_parser_defaults():
    args = build_parser().parse_args(["https://acme.fr"])
    assert args.jobs == 8
    assert args.timeout == 15.0
    assert args.format == "csv"
    assert args.region is None
    assert args.insecure is False


def test_parse_regions():
    assert parse_regions(None) is None
    assert parse_regions("") is None
    assert parse_regions("fr") == ("FR",)
    assert parse_regions("fr, us") == ("FR", "US")


@pytest.mark.parametrize("bad", ["FRA", "1U", "F"])
def test_parse_regions_rejects_bad_codes(bad):
    with pytest.raises(SystemExit):
        parse_regions(bad)


def test_harvest_marks_unreachable_leads():
    session = make_session()
    leads = harvest(["https://127.0.0.1:1"], session, jobs=1, timeout=1.0)
    assert len(leads) == 1
    assert leads[0].error
    assert leads[0].emails == []
