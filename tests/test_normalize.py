import pytest

from leadharvest.models import Lead
from leadharvest.normalize import clean_email, clean_phone, normalize_lead


@pytest.mark.parametrize(
    "raw",
    [
        "sales@acme.fr",
        "  First.Last+tag@sub.acme.co.uk  ",
        "hello@acme-studio.fr.",
        "contact@café-monde.info",
    ],
)
def test_clean_email_accepts_real_addresses(raw):
    assert clean_email(raw) is not None


@pytest.mark.parametrize(
    "raw",
    [
        "hero@2x.png",
        "style@1.css",
        "not-an-email@example-script.js",
        "user@localhost",
        "no-at-sign.example.com",
        "a@b..com",
        "@missing-local.com",
        "",
    ],
)
def test_clean_email_rejects_junk(raw):
    assert clean_email(raw) is None


@pytest.mark.parametrize(
    ("raw", "regions", "expected"),
    [
        ("+33 4 72 00 00 00", None, "+33472000000"),
        ("+44 20 7946 0958", None, "+442079460958"),
        ("+1 (800) 555-0199 ext. 88", None, "+18005550199"),
        ("tel:+33 4 72 00 00 00", None, "+33472000000"),
        ("04 72 00 00 00", ("FR",), "+33472000000"),
        ("06 12 34 56 78", ("FR",), "+33612345678"),
        ("(212) 555-0147", ("US",), "+12125550147"),
    ],
)
def test_clean_phone_returns_e164(raw, regions, expected):
    assert clean_phone(raw, regions) == expected


@pytest.mark.parametrize(
    ("raw", "regions"),
    [
        ("2024", None),
        ("12345", None),
        ("", None),
        ("call us", None),
        ("ISBN 978-3-16-148410-0", None),
        ("11111111", ("US",)),
        ("2026-11-03", ("US",)),
        ("505 160 26 10", ("US",)),
        ("112 33 11", ("US",)),
        ("04 72 00 00 00", None),
    ],
)
def test_clean_phone_rejects_junk(raw, regions):
    assert clean_phone(raw, regions) is None


def test_normalize_lead_dedupes_and_sorts():
    lead = Lead(
        url="https://acme.fr",
        name="  Acme  ",
        emails=["B@acme.fr", "a@acme.fr", "b@acme.fr", "hero@2x.png"],
        phones=["+33 4 72 00 00 00", "+33 4 72 00 00 00", "04 72 00 00 00", "2026-11-03"],
        social={"twitter": "https://x.com/acme", "linkedin": "https://linkedin.com/acme"},
    )
    out = normalize_lead(lead, regions=("FR",))
    assert out.name == "Acme"
    assert out.emails == ["a@acme.fr", "b@acme.fr"]
    assert out.phones == ["+33472000000"]
    assert list(out.social)[0] == "linkedin"


def test_lead_derives_domain_from_url():
    assert Lead(url="https://www.acme.fr/about").domain == "acme.fr"
