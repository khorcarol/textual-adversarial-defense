"""
Python tests for HomoglyphSanitizer based on C++ test cases.
"""

import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestHomoglyphSanitizer:
    """Test cases for homoglyph sanitization functionality."""

    def test_one_to_one_mappings(self):
        """Test that homoglyphs are replaced with their canonical forms."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_homoglyph_sanitizer()

        # Input: Greek Alpha (U+0391), Double Exclamation (U+001C3), Greek Beta (U+0392)
        # Expected: Latin A (U+0041), Exclamation (U+0021), Latin B (U+0042)
        text = chr(0x0391) + chr(0x001C3) + chr(0x0392)
        result = pipeline.sanitize(text)

        expected = chr(0x0041) + chr(0x0021) + chr(0x0042)  # 'A!B'
        assert result == expected, (
            f"Expected '{expected}' ({[hex(ord(c)) for c in expected]}), got '{result}' ({[hex(ord(c)) for c in result]})"
        )

    def test_no_mappings(self):
        """Test that text without homoglyphs remains unchanged."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_homoglyph_sanitizer()

        # Input: 'b', 'c', 'd' - regular ASCII characters
        text = "bcd"
        result = pipeline.sanitize(text)

        expected = "bcd"
        assert result == expected, f"Expected '{expected}', got '{result}'"
