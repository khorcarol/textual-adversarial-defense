from pathlib import Path
import json

"""
----------------
Bidi Attack Test
----------------
"""


# https://github.com/MeirKriheli/python-bidi


def python_bidi(pert):
    from bidi.algorithm import get_display

    disp = get_display(pert)
    return disp


def cpp_bidi(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_bidi_sanitizer()
    d2 = p.sanitize(pert)
    return d2


"""
----------------
Deletion Attack Test
----------------
"""
# TODO: cpp regex


def python_del(pert):
    res = []
    for c in pert:
        if c != "\x08":
            res.append(c)
        elif res:
            res.pop()
    return "".join(res)


# def python_del_regex(pert):
#     new_str = re.sub(r"^\x08|.\x08", "", pert)
#     return new_str


def cpp_del(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_deletion_sanitizer()
    d2 = p.sanitize(pert)
    return d2


"""
----------------
Homoglyph Attack Test
----------------
"""


# TODO: currently these use confusables.json
def python_homoglyph_homoglyphs(pert):
    import homoglyphs

    hg = homoglyphs.Homoglyphs()
    return hg.to_ascii(pert)


# TODO: currently these use confusables.json
def python_homoglyph_decancer(pert):
    from decancer_py import CuredString, parse

    parsed: CuredString = parse(pert)
    return parsed.__str__()


def cpp_homoglyph(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_homoglyph_sanitizer()
    d = p.sanitize(pert)
    return d


"""
----------------
Invisible Attack Test
----------------
"""
# https://github.com/SAFE-MCP/safe-mcp/blob/main/mitigations/SAFE-M-4/README.md
import unicodedata


class UnicodeSanitizer:
    # Define dangerous Unicode ranges
    INVISIBLE_CHARS = [
        "\u200b",  # Zero-width space
        "\u200c",  # Zero-width non-joiner
        "\u200d",  # Zero-width joiner
        "\u2060",  # Word joiner
        "\ufeff",  # Zero-width no-break space
    ]

    BIDI_CONTROL_CHARS = [
        "\u202a",  # Left-to-right embedding
        "\u202b",  # Right-to-left embedding
        "\u202c",  # Pop directional formatting
        "\u202d",  # Left-to-right override
        "\u202e",  # Right-to-left override
    ]

    # Private Use Area ranges
    PUA_RANGES = [
        (0xE000, 0xF8FF),  # BMP PUA
        (0xF0000, 0xFFFFF),  # Plane 15 PUA
        (0x100000, 0x10FFFF),  # Plane 16 PUA
        (0xE0000, 0xE007F),  # Unicode Tags
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        return cls._strict_sanitize(text)

    @classmethod
    def _strict_sanitize(cls, text: str) -> str:
        # Remove invisible characters
        for char in cls.INVISIBLE_CHARS:
            text = text.replace(char, "")

        # Remove bidirectional control
        for char in cls.BIDI_CONTROL_CHARS:
            text = text.replace(char, "")

        # Remove PUA characters
        cleaned = []
        for char in text:
            code_point = ord(char)
            in_pua = False
            for start, end in cls.PUA_RANGES:
                if start <= code_point <= end:
                    in_pua = True
                    break
            if not in_pua:
                cleaned.append(char)

        return "".join(cleaned)


def python_invisible_mcp(pert):
    return UnicodeSanitizer.sanitize(pert)


def cpp_invisible(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_invisible_sanitizer()
    d = p.sanitize(pert)
    return d


"""
----------------
Tag Attack Test
----------------
"""


# https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/
def python_tag_aws(input):
    return "".join(
        ch
        for ch in input
        # Unicode Tag block characters and high, low surrogates
        if not (0xE0000 <= ord(ch) <= 0xE007F or 0xD800 <= ord(ch) <= 0xDFFF)
    )


def cpp_tag(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_tag_sanitizer()
    d = p.sanitize(pert)
    return d


"""
----------------
Variation Selector Attack Test
----------------
"""


def _get_variation_selector_data():
    variation_selectors = set(range(0xFE00, 0xFE10))
    variation_selectors.update(range(0xE0100, 0xE01F0))
    resource_path = (
        Path(__file__).resolve().parents[1]
        / "utils"
        / "variation_selector"
        / "variation_selector.json"
    )
    with open(resource_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    allowed_prev = {}
    for key, values in data.items():
        cp = int(key.rstrip(";"), 16)
        allowed = allowed_prev.get(cp)
        if allowed is None:
            allowed = set()
            allowed_prev[cp] = allowed
        for v in values:
            allowed.add(int(v, 16))

    return variation_selectors, allowed_prev


def python_variation_selector(pert):
    variation_selectors, allowed_prev = _get_variation_selector_data()
    res = []
    prev_cp = None
    for ch in pert:
        cp = ord(ch)
        if cp in variation_selectors:
            allowed = allowed_prev.get(cp)
            if prev_cp is not None and allowed is not None and prev_cp in allowed:
                res.append(ch)
        else:
            res.append(ch)
        prev_cp = cp
    return "".join(res)


def cpp_variation_selector(pert):
    import textual_adversarial_defense

    p = textual_adversarial_defense._pipeline.Pipeline()
    p.add_variation_selector_sanitizer()
    d = p.sanitize(pert)
    return d
