emojis = "https://www.unicode.org/Public/17.0.0/ucd/emoji/emoji-variation-sequences.txt"
ivd  = "https://www.unicode.org/ivd/data/2025-07-14/IVD_Sequences.txt"
standardized_variants = "https://www.unicode.org/Public/17.0.0/ucd/StandardizedVariants.txt"

import requests
import json
from collections import defaultdict
allowed_previous_variations = defaultdict(list)


def load_from_file(link):
    resp = requests.get(link, stream=True)
    for line in resp.iter_lines():
        line_str = line.decode("utf-8")
        if len(line_str) == 0 or line_str[0] == "#":
            continue
        try:
            texts = line_str.split()
            prec, varselect = texts[0], texts[1]
        except:
            print(texts)
        allowed_previous_variations[varselect].append(prec)

load_from_file(emojis)
load_from_file(ivd)
load_from_file(standardized_variants)
with open("variation_selector.json", "w") as f:
    json.dump(allowed_previous_variations, f)
