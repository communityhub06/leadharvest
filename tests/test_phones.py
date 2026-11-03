from leadharvest.phones import phones_from_text

NOISY = """
Python 969 MIT 112 33 11 Updated Nov 3, 2026
Fibonacci 377 610 987 and 505 160 26 10 Updated Oct 30
Dated 2026-11-03 and 2026-11-07
Reach us on +33 4 72 00 00 00 or internationally +44 20 7946 0958
"""


def test_ignores_stats_dates_and_sequences():
    assert phones_from_text(NOISY) == ["+33472000000", "+442079460958"]


def test_default_region_captures_international_only():
    assert phones_from_text("call 06 12 34 56 78 today") == []
    assert phones_from_text("call +33 6 12 34 56 78 today") == ["+33612345678"]


def test_region_unlocks_national_numbers():
    assert phones_from_text("call 06 12 34 56 78 today", ("FR",)) == ["+33612345678"]


def test_deduplicates_across_regions():
    text = "US office +1 800 555 0199 and FR office +33 6 12 34 56 78"
    assert phones_from_text(text, ("US", "FR")) == ["+18005550199", "+33612345678"]


def test_empty_text():
    assert phones_from_text("") == []
