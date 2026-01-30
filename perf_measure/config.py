from python.generate_attack import (
    BidiAttack,
    DeletionCharAttack,
    HomoglyphAttack,
    InvisibleCharAttack,
    TagAttack,
    VariationSelectorAttack,
)
from perf_measure.functions import (
    python_bidi,
    cpp_bidi,
    python_del,
    cpp_del,
    python_homoglyph_homoglyphs,
    python_homoglyph_decancer,
    cpp_homoglyph,
    python_invisible_mcp,
    cpp_invisible,
    python_tag_aws,
    cpp_tag,
    python_variation_selector,
    cpp_variation_selector,
)


ATTACKS = {
    "bidi": {
        "attack_cls": BidiAttack,
        "impls": {
            "python": python_bidi,
            "cpp": cpp_bidi,
        },
    },
    "deletion": {
        "attack_cls": DeletionCharAttack,
        "impls": {
            "python": python_del,
            "cpp": cpp_del,
        },
    },
    "homoglyph": {
        "attack_cls": HomoglyphAttack,
        "impls": {
            "homoglyphs": python_homoglyph_homoglyphs,
            "decancer": python_homoglyph_decancer,
            "cpp": cpp_homoglyph,
        },
    },
    "invisible": {
        "attack_cls": InvisibleCharAttack,
        "impls": {
            "python_mcp": python_invisible_mcp,
            "cpp": cpp_invisible,
        },
    },
    "tag": {
        "attack_cls": TagAttack,
        "impls": {
            "python_aws": python_tag_aws,
            "cpp": cpp_tag,
        },
    },
    "variation": {
        "attack_cls": VariationSelectorAttack,
        "impls": {
            "python": python_variation_selector,
            "cpp": cpp_variation_selector,
        },
    },
}
