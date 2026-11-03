from leadharvest.extract import extract, social_platform

SAMPLE = """
<html><head>
<title>Acme Studio — Web design in Lyon</title>
<meta name="description" content="Acme Studio builds fast websites for small businesses.">
<meta property="og:site_name" content="Acme Studio">
</head><body>
<a href="mailto:hello@acme-studio.fr?subject=hi">email us</a>
<a href="tel:+33 4 72 00 00 00">call</a>
<a href="https://www.linkedin.com/company/acme-studio">in</a>
<a href="https://x.com/acmestudio">tw</a>
<p>Press sales@acme-studio.fr or +33 4 72 00 00 00.</p>
<img src="/assets/hero@2x.png">
<script>var fake = "not-an-email@example-script.js";</script>
</body></html>
"""


def test_extracts_site_name_from_og():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert out.name == "Acme Studio"


def test_extracts_description():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert out.description.startswith("Acme Studio builds")


def test_finds_mailto_and_text_emails():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert "hello@acme-studio.fr" in out.emails
    assert "sales@acme-studio.fr" in out.emails


def test_finds_tel_and_text_phones():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert any("33472000000" in p.replace(" ", "") for p in out.phones)


def test_social_links_absolutised():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert out.social["linkedin"] == "https://www.linkedin.com/company/acme-studio"
    assert out.social["twitter"] == "https://x.com/acmestudio"


def test_script_content_is_ignored():
    out = extract(SAMPLE, "https://acme-studio.fr")
    assert not any(e.endswith("example-script.js") for e in out.emails)


def test_social_platform_matches_subdomains():
    assert social_platform("https://m.facebook.com/acme") == "facebook"
    assert social_platform("https://youtu.be/abc") == "youtube"
    assert social_platform("https://acme-studio.fr") is None


def test_handles_bytes_and_messy_html():
    messy = "<html><body><h1>  Tiny   Shop  </h1><a href='mailto:buy@tiny.shop'>x</a></body></html>"
    out = extract(messy, "https://tiny.shop")
    assert out.name == "Tiny Shop"
    assert out.emails == ["buy@tiny.shop"]
