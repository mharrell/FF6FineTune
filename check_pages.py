import json

with open("data/raw/ff6_wiki_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Pages in raw file: {len(data)}")
for page in data:
    print(f"  {page['title']}")