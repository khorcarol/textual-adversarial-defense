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

with open("confusables.json", "w") as f:
    json.dump(confusables, f)
