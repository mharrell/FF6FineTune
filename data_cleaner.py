import json
import re
import os

SKIP_HEADINGS = {
    "citations", "see also", "external links",
    "references", "notes",
    "unlisted entries", "dummied",
    "gallery",
    "non-final fantasy guest appearances",
    "unused weapons",
    "packaging artwork",
    "production credits",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
}


def clean_text(text):
    # Remove ref tags and their contents
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^>]*/>', '', text)

    # Remove gallery blocks
    text = re.sub(r'<gallery>.*?</gallery>', '', text, flags=re.DOTALL)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove infobox/template blocks (multiple passes for nesting)
    for _ in range(5):
        text = re.sub(r'\{\{[^{}]*\}\}', '', text)

    # Remove file/image links
    text = re.sub(r'\[\[File:[^\]]*\]\]', '', text)
    text = re.sub(r'\[\[Image:[^\]]*\]\]', '', text)

    # Convert [[link|display]] to display text
    text = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', text)

    # Convert [[link]] to link text
    text = re.sub(r'\[\[([^\]]*)\]\]', r'\1', text)

    # Remove external links [http://... text] -> text
    text = re.sub(r'\[https?://[^\s\]]+\s([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[https?://[^\]]+\]', '', text)

    # Remove table markup
    text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
    text = re.sub(r'^\s*[|!].*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\|-', '', text)

    # Remove wiki formatting
    text = re.sub(r"'{2,3}", '', text)
    text = re.sub(r'={2,6}[^=]+=+', '', text)

    # Remove category/navbox/language links
    text = re.sub(r'\[\[Category:[^\]]*\]\]', '', text)
    text = re.sub(r'\[\[[a-z\-]+:[^\]]*\]\]', '', text)
    text = re.sub(r'\{\{navbox[^}]*\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{citations\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{spoiler[^}]*\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{endspoiler\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{Quote\|[^}]*\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{[Ss]ee\|[^}]*\}\}', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{\{main\|[^}]*\}\}', '', text, flags=re.IGNORECASE)

    # Remove [TABLE ROW: ...] artifacts
    text = re.sub(r'\[TABLE ROW:[^\]]*\]', '', text)

    # Remove leftover image caption artifacts
    text = re.sub(r'^\s*\.\]\]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\.\]\]', '', text)

    # Remove image filename patterns
    text = re.sub(r'\S+\.png\|[^\n]+', '', text)
    text = re.sub(r'\S+\.gif\|[^\n]+', '', text)
    text = re.sub(r'\S+\.jpg\|[^\n]+', '', text)

    # Clean up bullet asterisks
    text = re.sub(r'^\s*\*+\s*', '- ', text, flags=re.MULTILINE)

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    return text


def clean_data(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned_data = []

    for page in raw_data:
        cleaned_page = {
            "title": page["title"],
            "url": page["url"],
            "sections": []
        }

        for section in page["sections"]:
            # Skip unhelpful sections
            if section["heading"].lower() in SKIP_HEADINGS:
                continue

            cleaned_content = clean_text(section["content"])

            # Skip sections that are basically empty after cleaning
            if len(cleaned_content) < 20:
                continue

            cleaned_page["sections"].append({
                "heading": section["heading"],
                "content": cleaned_content,
                "versions": section["versions"]
            })

        # Skip disambiguation or near-empty pages
        total_content = " ".join(s["content"] for s in cleaned_page["sections"])
        if len(total_content) < 50:
            print(f"  -> Skipping (too little content): {page['title']} ({len(total_content)} chars)")
            continue

        if cleaned_page["sections"]:
            cleaned_data.append(cleaned_page)

        print(f"Cleaned: {page['title']} -> {len(cleaned_page['sections'])} sections")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Saved {len(cleaned_data)} pages to {output_path}")


if __name__ == "__main__":
    clean_data("data/raw/ff6_wiki_raw.json", "data/cleaned/ff6_wiki_cleaned.json")