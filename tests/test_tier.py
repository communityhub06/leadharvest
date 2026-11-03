import pytest

from leadharvest import tier
from leadharvest.cli import build_parser, enforce_tier, main
from leadharvest.extract import extract


def test_free_build_limits():
    assert tier.PRO is False
    assert tier.MAX_URLS == 25
    assert tier.FORMATS == ("csv",)
    assert tier.CRAWL is False
    assert tier.REGIONS is False
    assert tier.SOCIAL == frozenset(("linkedin", "twitter", "facebook", "instagram", "github"))
    assert tier.edition() == "Free"


def test_blocked_message_names_the_feature_and_the_store():
    message = tier.blocked("--format json", "JSON and dual export are included")
    assert "--format json" in message
    assert "Pro feature" in message
    assert tier.UPGRADE_URL in message


@pytest.mark.parametrize("argv", [["--format", "json"], ["--format", "both"]])
def test_free_rejects_json_export(argv):
    with pytest.raises(SystemExit) as exc:
        enforce_tier(build_parser().parse_args(argv))
    assert "Pro feature" in str(exc.value)


def test_free_rejects_crawl_mode():
    with pytest.raises(SystemExit) as exc:
        enforce_tier(build_parser().parse_args(["--domain", "acme.fr"]))
    assert "--domain" in str(exc.value)


def test_free_rejects_region_hint():
    with pytest.raises(SystemExit) as exc:
        enforce_tier(build_parser().parse_args(["--region", "FR"]))
    assert "--region" in str(exc.value)


def test_free_accepts_the_plain_csv_invocation():
    enforce_tier(build_parser().parse_args(["https://acme.fr", "--region", None]))


def test_free_rejects_more_urls_than_the_cap(tmp_path):
    listing = tmp_path / "urls.txt"
    listing.write_text("\n".join(f"https://site{i}.com" for i in range(26)), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["-i", str(listing), "--quiet"])
    assert "25" in str(exc.value)
    assert tier.UPGRADE_URL in str(exc.value)


def test_free_runs_exactly_the_cap(monkeypatch, tmp_path):
    monkeypatch.setattr("leadharvest.cli.harvest", lambda *a, **k: [])
    listing = tmp_path / "urls.txt"
    listing.write_text("\n".join(f"https://site{i}.com" for i in range(25)), encoding="utf-8")
    out = tmp_path / "leads.csv"
    assert main(["-i", str(listing), "--quiet", "-o", str(out)]) == 0
    assert out.exists()


def test_free_harvests_only_the_five_included_platforms():
    html = """
    <html><head><title>Acme</title></head><body>
      <a href="https://www.linkedin.com/company/acme">in</a>
      <a href="https://github.com/acme">gh</a>
      <a href="https://t.me/acme">tg</a>
      <a href="https://www.youtube.com/@acme">yt</a>
      <a href="https://www.pinterest.com/acme">pin</a>
    </body></html>
    """
    social = extract(html, "https://acme.com").social
    assert tier.SOCIAL is not None
    assert set(social) <= tier.SOCIAL
    assert "linkedin" in social and "github" in social
    assert "telegram" not in social
    assert "youtube" not in social
    assert "pinterest" not in social
