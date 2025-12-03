import sys
from pathlib import Path

here = Path(__file__).parent.resolve()
sys.path.insert(0, str(here))

import _pipeline  # the compiled extension

def codepoints_ord(s: str):
    return [f"U+{ord(ch):04X}" for ch in s]

# Bidi => Invisible
p = _pipeline.Pipeline()
p.add_bidi_sanitizer()
p.add_invisible_sanitizer()
p.add_tag_sanitizer()
p.add_homoglyph_sanitizer()
bidi = "Hello \u202eWorld \u202c \u200b \u0430"

print(codepoints_ord(bidi))
print(bidi)
print(codepoints_ord(p.sanitize(bidi))) 
print(p.sanitize(bidi))

p = _pipeline.Pipeline()
p.add_tag_sanitizer()

t = "\U000e0047"
print(codepoints_ord(p.sanitize(t)))

