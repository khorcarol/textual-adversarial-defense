import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestBidiSanitizer:
    """Test cases for Bidi sanitization functionality."""

    def test_reorders_rlo_segment(self):
        """Test that RLO segments are correctly reordered."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_bidi_sanitizer()

        # Input: RLO + 'd','l','r','o','W' + PDF
        # Expected: RLO + 'W','o','r','l','d' + PDF (reversed)
        text = chr(0x202E) + "dlroW" + chr(0x202C)
        result = pipeline.sanitize(text)

        expected = chr(0x202E) + "World" + chr(0x202C)
        assert result == expected, f"Expected '{expected}', got '{result}'"
