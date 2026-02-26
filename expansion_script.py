# DANGER THIS SCRIPT COSTS MONEY

import json
import os
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def expand_pairs(input_jsonl, cleaned_json, output_jsonl):
    # Load existing pairs so we don't duplicate
    existing_instructions = set()
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            pair = json.loads(line)
            existing_instructions.add(pair["instruction"])

    # Load cleaned data
    with open(cleaned_json, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    new_pairs = []
    total_sections = sum(len(p["sections"]) for p in cleaned_data)
    processed = 0

    for page in cleaned_data:
        title = page["title"].replace("_", " ").replace("(Final Fantasy VI)", "").strip()
        title = title.replace("(summon)", "").replace("(command)", "").strip()

        for section in page["sections"]:
            content = section["content"]
            heading = section["heading"]

            # Skip very short sections
            if len(content) < 50:
                continue

            processed += 1
            print(f"Processing ({processed}/{total_sections}): {title} - {heading}")

            prompt = f"""You are helping build a question/answer training dataset for a Final Fantasy VI game guide AI.

Given this content about "{title}" (section: "{heading}"):

{content[:800]}

Generate 3 natural questions a player might ask about this, along with their answers based only on the content above.
Format your response as JSON array like this:
[
  {{"question": "...", "answer": "..."}},
  {{"question": "...", "answer": "..."}},
  {{"question": "...", "answer": "..."}}
]

Rules:
- Questions should be natural things a player would ask
- Answers should be based only on the provided content
- Do not repeat these existing questions: {list(existing_instructions)[:5]}
- Return ONLY the JSON array, no other text"""

            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=600,
                    messages=[{"role": "user", "content": prompt}]
                )

                text = response.content[0].text.strip()
                # Strip markdown code blocks if present
                text = text.replace("```json", "").replace("```", "").strip()
                generated = json.loads(text)

                for item in generated:
                    q = item.get("question", "").strip()
                    a = item.get("answer", "").strip()
                    if q and a and q not in existing_instructions:
                        new_pairs.append({
                            "instruction": q,
                            "input": "",
                            "output": a
                        })
                        existing_instructions.add(q)

            except Exception as e:
                print(f"  -> Error: {e}")
                continue

            # Be polite to the API
            time.sleep(0.5)

    # Append new pairs to existing file
    with open(output_jsonl, 'a', encoding='utf-8') as f:
        for pair in new_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\nGenerated {len(new_pairs)} new pairs.")
    print(f"Total pairs now in {output_jsonl}")


if __name__ == "__main__":
    expand_pairs(
        "data/training/ff6_training_pairs.jsonl",
        "data/cleaned/ff6_wiki_cleaned.json",
        "data/training/ff6_training_pairs.jsonl"
    )