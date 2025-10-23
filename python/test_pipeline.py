import sys
from pathlib import Path

here = Path(__file__).parent.resolve()
sys.path.insert(0, str(here))

import _pipeline  # the compiled extension

def codepoints_ord(s: str):
    return [f"U+{ord(ch):04X}" for ch in s]

# before = "a\u200bb"
# after = _pipeline.sanitize_with_invisible(before)

# print("Before codepoints:", codepoints_ord(before))
# print("After  codepoints:", codepoints_ord(after))

# Example output:
# Before codepoints: ['U+0061', 'U+200B', 'U+0062']
# After  codepoints: ['U+0061', 'U+0062']

# p = _pipeline.Pipeline()
# p.add_invisible_sanitizer()
# print(p.sanitize("a\u200bb"))  #"ab"


# Bidi => Invisible
p = _pipeline.Pipeline()
p.add_bidi_sanitizer()
p.add_invisible_sanitizer()
p.add_tag_sanitizer()
bidi = "Hello \u202eWorld \u202c \u200b"

print(codepoints_ord(bidi))
print(bidi)
print(codepoints_ord(p.sanitize(bidi))) 
print(p.sanitize(bidi))

