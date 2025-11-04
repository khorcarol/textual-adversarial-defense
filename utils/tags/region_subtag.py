import json
import xml.etree.ElementTree as ET
import os
import re

# Expand tokens like '001~3"
def expand_token(token):
    if "~" not in token:
        return [token.strip()]
    start, end = token.split("~")
    start, end = start.strip(), end.strip()

    expanded = []
    if start[-1].isdigit() and end[0].isdigit():
        for i in range(int(start[-1]), int(end[0]) + 1):
            expanded.append(f"{start[:-1]}{i}{end[1:]}")

    return expanded


# Load the XML file
base_dir = os.path.dirname(__file__)
xml_path = os.path.join(base_dir, "region.xml")
tree = ET.parse(xml_path)
root = tree.getroot()

# Regex for three digit numbers (accoutning for tilde ranges)
regex = r"\b(?:(?:\d{1})~(?:\d{3})\b|\b(?:\d{2})~(?:\d{2})\b|\b(?:\d{3})~(?:\d{1}))\b|\b(?:\d{3})\b"
pattern = re.compile(regex)
region_subtags = []

for elem in root.findall(".//id[@type='region']"):
    if elem.text:
        raw_text = elem.text
        matches = pattern.findall(raw_text)
        for match in matches:
            expanded_codes = expand_token(match)
            region_subtags.extend(expanded_codes)

with open("region_subtags.json", "w") as f:
    json.dump(region_subtags, f)


