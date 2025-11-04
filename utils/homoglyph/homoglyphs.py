import requests
import json
confusables = dict()

conf_resp = requests.get(
    "https://www.unicode.org/Public/security/latest/confusables.txt", stream=True
)
for line in conf_resp.iter_lines():
    if len(line):
        line = line.decode("utf-8-sig")
        if line[0] != "#":
            fields = line.split(";")
            src = fields[0].strip()
            dst = fields[1].strip()
            confusables[src] = dst

with open("generated_homoglyph.cpp", "w") as f:
    f.write("#include <unordered_map>\n")
    f.write("#include <modules/homoglyph.h>\n")
    f.write(
        "const std::unordered_map<char32_t, std::vector<char32_t>> HomoglyphSanitizer::homoglyph_map = {\n"
    )
    
    for key, values in confusables.items():
        k = "{0x"+key+"}"
        s = ["0x"+value for value in values.split()]
        v = "{"+ ", ".join(s) + "}"
        f.write(f"  {{{k}, {v}}},\n")
    f.write("};\n")
