from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
 "textattack/roberta-base-SST-2"
)

special_chars = {
    # Variation selectors (U+FE00–U+FE0F, U+E0100–U+E01EF)
    "variation_selectors": [chr(cp) for cp in list(range(0xFE00, 0xFE10)) + list(range(0xE0100, 0xE01F0))],

    # Unicode “tag” characters (U+E0000–U+E001F)
    "tag_characters": [chr(0xE0000 + i) for i in range(32)],

    # Typical invisible characters
    "invisible_characters": [
        "\u200B",  # zero-width space
        "\u200C",  # zero-width non-joiner
        "\u200D",  # zero-width joiner
        "\u061C",  # Arabic letter mark
        "\u180E",  # Mongolian vowel separator
    ],

    # Bidi control characters
    "bidi_characters": [
        "\u202A", "\u202B", "\u202C", "\u202D", "\u202E"
    ],
    
    "deletion_character": ["\u0008"]

}

for category, chars in special_chars.items():
    for char in chars:
        enc = tokenizer(
            char,
            return_tensors="pt",   # or "tf"/"np"
            truncation=True,
            max_length=128
        )
        print(f"Category: {category}, Char: {repr(char)}, Encoded: {enc}")


