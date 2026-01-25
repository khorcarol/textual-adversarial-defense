import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestCombinedSanitizer:
    """Test cases for combined sanitizer functionality."""

    # Test homoglyph functionality in combined sanitizer
    def test_combined_one_to_one_mappings(self):
        """Test that homoglyphs are replaced with their canonical forms."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Input: Greek Alpha (U+0391), Double Exclamation (U+001C3), Greek Beta (U+0392)
        # Expected: Latin A (U+0041), Exclamation (U+0021), Latin B (U+0042)
        text = chr(0x0391) + chr(0x001C3) + chr(0x0392)
        result = pipeline.sanitize(text)

        expected = chr(0x0041) + chr(0x0021) + chr(0x0042)  # 'A!B'
        assert result == expected, (
            f"Expected '{expected}' ({[hex(ord(c)) for c in expected]}), got '{result}' ({[hex(ord(c)) for c in result]})"
        )

    def test_combined_no_mappings(self):
        """Test that text without homoglyphs remains unchanged."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Input: 'b', 'c', 'd' - regular ASCII characters
        text = "bcd"
        result = pipeline.sanitize(text)

        expected = "bcd"
        assert result == expected, f"Expected '{expected}', got '{result}'"

    # Test invisible characters in combined sanitizer
    def test_combined_removes_zero_width_space(self):
        """Test that zero-width space (ZWSP) is removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Input: "a<ZWSP>b" where ZWSP is U+200B
        text = "a" + chr(0x200B) + "b"
        result = pipeline.sanitize(text)

        expected = "ab"
        assert result == expected, f"Expected '{expected}', got '{result}'"

    def test_combined_preserve_characters(self):
        """Test that normal characters are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        text = "ab"
        result = pipeline.sanitize(text)

        expected = "ab"
        assert result == expected, f"Expected '{expected}', got '{result}'"

    # Test tags in combined sanitizer
    def test_combined_valid_tag_sequence(self):
        """Test that valid tag sequences are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

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

    def test_combined_tag_outside_base(self):
        """Test that tag characters without base are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

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

    def test_combined_invalid_tag_sequence(self):
        """Test that invalid tag sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

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

    def test_combined_no_tags(self):
        """Test that text without tags remains unchanged."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        text = "hello world"
        result = pipeline.sanitize(text)
        expected = "hello world"

        assert result == expected, f"Expected '{expected}', got '{result}'"

    def test_combined_too_long_tag_sequence(self):
        """Test that excessively long tag sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Create a sequence longer than MAX_TAG_LENGTH (33 tags)
        text = chr(0x1F3F4)  # Base character
        for i in range(33):  # 33 > MAX_TAG_LENGTH
            text += chr(0xE0000 + ord("a"))
        text += chr(0xE007F)  # Cancel tag

        result = pipeline.sanitize(text)
        expected = ""  # Should be removed

        assert result == expected, f"Expected empty string, got '{result}'"

    # Test variation selectors in combined sanitizer
    def test_combined_valid_variation_sequence(self):
        """Test that valid variation selector sequences are preserved."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Valid variation sequence: # (U+0023) + VS-16 (U+FE0F)
        text = chr(0x0023) + chr(0xFE0F)
        result = pipeline.sanitize(text)

        expected = chr(0x0023) + chr(0xFE0F)
        assert result == expected, f"Expected valid variation sequence to be preserved"

    def test_combined_invalid_variation_sequence(self):
        """Test that invalid variation selector sequences are removed."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_combined_sanitizer()

        # Invalid variation sequence
        text = chr(0x0001) + chr(0xFE0F) + chr(0xE01EF)
        result = pipeline.sanitize(text)

        # Only the first character should remain (invalid VS removed)
        expected = chr(0x0001)
        assert result == expected, f"Expected '{repr(expected)}', got '{repr(result)}'"

   