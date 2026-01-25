"""
Python tests for DeletionCharSanitizer based on C++ test cases.
"""

import pytest

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestDeletionSanitizer:
    """Test cases for deletion sanitization functionality."""

    def test_deletion(self):
        """Test that control characters are deleted."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_deletion_sanitizer()

        # Input: control characters 0x3, 0x1, 0x2, 0x8, 0x8, 0x9
        # Expected: only 0x3 and 0x9 remain
        text = chr(0x3) + chr(0x1) + chr(0x2) + chr(0x8) + chr(0x8) + chr(0x9)
        result = pipeline.sanitize(text)

        expected = chr(0x3) + chr(0x9)
        assert result == expected, (
            f"Expected codepoints {[ord(c) for c in expected]}, got {[ord(c) for c in result]}"
        )

    def test_no_deletions(self):
        """Test that text without deletable characters remains unchanged."""
        pipeline = textual_adversarial_defense._pipeline.Pipeline()
        pipeline.add_deletion_sanitizer()

        text = chr(0x3) + chr(0x9)
        result = pipeline.sanitize(text)

        expected = chr(0x3) + chr(0x9)
        assert result == expected, (
            f"Expected codepoints {[ord(c) for c in expected]}, got {[ord(c) for c in result]}"
        )
