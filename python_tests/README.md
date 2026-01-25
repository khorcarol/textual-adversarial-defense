
Pytest test suite for textual-adversarial-defense.

Test modules:
- test_bidi.py: Tests for bidirectional text sanitization
- test_deletion.py: Tests for deletion character sanitization
- test_homoglyph.py: Tests for homoglyph sanitization
- test_invisible.py: Tests for invisible character sanitization
- test_tags.py: Tests for tag character sanitization
- test_variation_selector.py: Tests for variation selector sanitization
- test_combined.py: Tests for combined sanitizer functionality

To run all tests:
    pytest python_tests/

To run a specific test module:
    pytest python_tests/test_invisible.py

To run with verbose output:
    pytest python_tests/ -v
