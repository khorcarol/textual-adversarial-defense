"""
Python tests for TagCharSanitizer based on C++ test cases.
"""

import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestTagSanitizer:
    """Test cases for tag character sanitization functionality."""

    def test_valid_tag_sequence(self):
        """Test that valid tag sequences are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_tag_sanitizer()

        # Valid emoji flag tag sequence for England (gbeng)
        text = (
            chr(0x1F3F4)  # Black flag emoji
            + chr(0xE0000 + ord("g"))
            + chr(0xE0000 + ord("b"))
            + chr(0xE0000 + ord("e"))
            + chr(0xE0000 + ord("n"))
            + chr(0xE0000 + ord("g"))
            + chr(0xE007F)
        )  # Cancel tag

        result = pipeline.sanitize(text)
        expected = text  # Should remain unchanged

        assert result == expected, f"Expected valid tag sequence to be preserved"

    def test_tag_outside_base(self):
        """Test that tag characters without base are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_tag_sanitizer()

        # Tags without base character
        text = (
            chr(0xE0000 + ord("g"))
            + chr(0xE0000 + ord("b"))
            + chr(0xE0000 + ord("e"))
            + chr(0xE0000 + ord("n"))
            + chr(0xE0000 + ord("g"))
        )

        result = pipeline.sanitize(text)
        expected = ""  # Should be removed

        assert result == expected, f"Expected empty string, got '{result}'"

    def test_invalid_tag_sequence(self):
        """Test that invalid tag sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_tag_sanitizer()

        # Invalid tag sequence (abc is not a valid sequence)
        text = (
            chr(0x1F3F4)  # Black flag emoji
            + chr(0xE0000 + ord("a"))
            + chr(0xE0000 + ord("b"))
            + chr(0xE0000 + ord("c"))
            + chr(0xE007F)
        )  # Cancel tag

        result = pipeline.sanitize(text)
        expected = ""  # Invalid sequence should be removed

        assert result == expected, f"Expected empty string, got '{result}'"

    def test_no_tags(self):
        """Test that text without tags remains unchanged."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_tag_sanitizer()

        text = "hello world"
        result = pipeline.sanitize(text)
        expected = "hello world"

        assert result == expected, f"Expected '{expected}', got '{result}'"

    def test_too_long_tag_sequence(self):
        """Test that excessively long tag sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_tag_sanitizer()

        # Create a sequence longer than MAX_TAG_LENGTH (33 tags)
        text = chr(0x1F3F4)  # Base character
        for i in range(33):  # 33 > MAX_TAG_LENGTH
            text += chr(0xE0000 + ord("a"))
        text += chr(0xE007F)  # Cancel tag

        result = pipeline.sanitize(text)
        expected = ""  # Should be removed

        assert result == expected, f"Expected empty string, got '{result}'"
