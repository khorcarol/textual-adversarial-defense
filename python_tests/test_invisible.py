"""
Python tests for InvisibleCharSanitizer based on C++ test cases.
"""

import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestInvisibleCharSanitizer:
    """Test cases for invisible character sanitization functionality."""

    def test_removes_zero_width_space(self):
        """Test that zero-width space (ZWSP) is removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_invisible_sanitizer()

        # Input: "a<ZWSP>b" where ZWSP is U+200B
        text = "a" + chr(0x200B) + "b"
        result = pipeline.sanitize(text)

        expected = "ab"
        assert result == expected, f"Expected '{expected}', got '{result}'"

    def test_preserve_characters(self):
        """Test that normal characters are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_invisible_sanitizer()

        text = "ab"
        result = pipeline.sanitize(text)

        expected = "ab"
        assert result == expected, f"Expected '{expected}', got '{result}'"
