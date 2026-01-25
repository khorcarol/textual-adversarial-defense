"""
Python tests for VariationSelectorSanitizer based on C++ test cases.
"""

import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestVariationSelectorSanitizer:
    """Test cases for variation selector sanitization functionality."""

    def test_valid_variation_sequence(self):
        """Test that valid variation selector sequences are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_variation_selector_sanitizer()

        # Valid variation sequence: # (U+0023) + VS-16 (U+FE0F)
        text = chr(0x0023) + chr(0xFE0F)
        result = pipeline.sanitize(text)

        expected = chr(0x0023) + chr(0xFE0F)
        assert result == expected, f"Expected valid variation sequence to be preserved"

    def test_invalid_variation_sequence(self):
        """Test that invalid variation selector sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_variation_selector_sanitizer()

        # Invalid variation sequence
        text = chr(0x0001) + chr(0xFE0F) + chr(0xE01EF)
        result = pipeline.sanitize(text)

        # Only the first character should remain (invalid VS removed)
        expected = chr(0x0001)
        assert result == expected, f"Expected '{repr(expected)}', got '{repr(result)}'"

    def test_invalid_variation_sequence(self):
        """Test that invalid variation selector sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_variation_selector_sanitizer()

        # Invalid variation sequence
        text = chr(0x0001) + chr(0xFE0F)
        result = pipeline.sanitize(text)

        # Only the first character should remain (invalid VS removed)
        expected = chr(0x0001)
        assert result == expected, f"Expected '{repr(expected)}', got '{repr(result)}'"
