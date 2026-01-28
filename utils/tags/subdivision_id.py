import json
import xml.etree.ElementTree as ET
import os
import string


# Expand tokens like 'ad02~8', 'zwmv~w', 'alpq~r'
def expand_token(token):
    if "~" not in token:
        return [token.strip()]
    start, end = token.split("~")
    start, end = start.strip(), end.strip()

    expanded = []
    # Case 1: numeric suffix
    if start[-1].isdigit() and end[0].isdigit():
        for i in range(int(start[-1]), int(end[0]) + 1):
            expanded.append(f"{start[:-1]}{i}{end[1:]}")

    # Case 2: alphabetic suffix
    elif start[-1].isalpha() and end[0].isalpha():
        alphabet = string.ascii_lowercase
        for c in range(alphabet.index(start[-1]), alphabet.index(end[0]) + 1):
            expanded.append(f"{start[:-1]}{alphabet[c]}{end[1:]}")
    return expanded


# Load the XML file
base_dir = os.path.dirname(__file__)
xml_path = os.path.join(base_dir, "subdivision.xml")

tree = ET.parse(xml_path)
root = tree.getroot()

# Get regular subdivision IDs
regular = root.find(".//id[@type='subdivision'][@idStatus='regular']")
if regular is not None and regular.text:
    raw_text = regular.text.strip()
    tokens = raw_text.split()
    regular_subdivision_ids = [code for token in tokens for code in expand_token(token)]

# Get deprecated subdivision IDs
deprecated = root.find(".//id[@type='subdivision'][@idStatus='deprecated']")
if deprecated is not None and deprecated.text:
    raw_text = deprecated.text.strip()
    tokens = raw_text.split()
    deprecated_subdivision_ids = [
        code for token in tokens for code in expand_token(token)
    ]

all = regular_subdivision_ids + deprecated_subdivision_ids
with open("subdivision_ids.json", "w") as f:
    # json.dump(regular_subdivision_ids, f)
    # json.dump(deprecated_subdivision_ids, f)
    json.dump(all, f)
