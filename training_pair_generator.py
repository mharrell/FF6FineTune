import json
import os
import random

def generate_training_pairs(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    training_pairs = []

    for page in cleaned_data:
        title = page["title"].replace("_", " ").replace("(Final Fantasy VI)", "").replace("Final Fantasy VI", "").strip()
        title = title.replace("(summon)", "").replace("(command)", "").strip()

        for section in page["sections"]:
            content = section["content"]
            heading = section["heading"]
            versions = section["versions"]

            # Build version context string
            if "all_versions" in versions:
                version_note = ""
            else:
                version_map = {
                    "snes": "SNES",
                    "ps1": "PlayStation",
                    "gba": "GBA",
                    "ios": "iOS/Android",
                    "steam": "Steam",
                    "pixel_remaster": "Pixel Remaster"
                }
                version_names = [version_map.get(v, v) for v in versions]
                version_note = f" (applies to: {', '.join(version_names)})"

            # Skip very short content
            if len(content) < 30:
                continue

            h = heading.lower()

            # INTRODUCTION
            if h == "introduction":
                pairs = [
                    {
                        "instruction": f"Who is {title}?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Tell me about {title} in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Give me an overview of {title} in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # GAMEPLAY
            elif h == "gameplay":
                pairs = [
                    {
                        "instruction": f"How does {title} work in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What are {title}'s gameplay mechanics in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Is {title} useful in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # MECHANICS
            elif h == "mechanics":
                pairs = [
                    {
                        "instruction": f"How does the {title} mechanic work in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Explain the {title} system in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What are the rules for {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # STORY / HISTORY / SYNOPSIS
            elif h in ["story", "history", "synopsis"]:
                pairs = [
                    {
                        "instruction": f"What is the story of {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What happens to {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What is the background of {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # CHARACTERISTICS
            elif h == "characteristics":
                pairs = [
                    {
                        "instruction": f"What are the characteristics and personality of {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Describe {title}'s appearance and personality in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What does {title} look like in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # PROFILE
            elif h == "profile":
                pairs = [
                    {
                        "instruction": f"What is the profile of {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Describe {title} in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # LAYOUT
            elif h == "layout":
                pairs = [
                    {
                        "instruction": f"What does {title} look like in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Describe the layout of {title} in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # LOCATIONS
            elif h in ["locations", "territories"]:
                pairs = [
                    {
                        "instruction": f"What locations are in {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Where is {title} located in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # OBTAINED
            elif h == "obtained":
                pairs = [
                    {
                        "instruction": f"How do I get {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Where can I find {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"How do I obtain {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # MAPS
            elif h == "maps":
                pairs = [
                    {
                        "instruction": f"What does the map of {title} look like in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # USE
            elif h == "use":
                pairs = [
                    {
                        "instruction": f"How do I use {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What is {title} used for in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # LIST sections
            elif h.startswith("list of"):
                pairs = [
                    {
                        "instruction": f"What are the {h} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"Can you list all {h} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # RELEASES / DEVELOPMENT / LOCALIZATION
            elif h in ["releases", "development", "localization"]:
                pairs = [
                    {
                        "instruction": f"What are the different versions of {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"How did {title} change between versions of Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # BEHIND THE SCENES
            elif h == "behind the scenes":
                pairs = [
                    {
                        "instruction": f"What are some behind the scenes facts about {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # MUSICAL THEMES
            elif h == "musical themes":
                pairs = [
                    {
                        "instruction": f"What music plays in {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                    {
                        "instruction": f"What is the musical theme for {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # ETYMOLOGY
            elif h in ["etymology", "etymology and symbolism"]:
                pairs = [
                    {
                        "instruction": f"What is the origin of the name {title} in Final Fantasy VI?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # OTHER APPEARANCES
            elif h == "other appearances":
                pairs = [
                    {
                        "instruction": f"Does {title} appear in other Final Fantasy games?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # OTHER MEDIA / MERCHANDISE
            elif h in ["other media", "merchandise"]:
                pairs = [
                    {
                        "instruction": f"Has {title} from Final Fantasy VI appeared in other media or merchandise?",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            # DEFAULT
            else:
                pairs = [
                    {
                        "instruction": f"Tell me about the {heading} of {title} in Final Fantasy VI.",
                        "input": "",
                        "output": content + version_note
                    },
                ]

            training_pairs.extend(pairs)

    # Shuffle for better training
    random.shuffle(training_pairs)

    # Save as JSONL
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"Generated {len(training_pairs)} training pairs.")
    print(f"Saved to {output_path}")
    return training_pairs


if __name__ == "__main__":
    generate_training_pairs(
        "data/cleaned/ff6_wiki_cleaned.json",
        "data/training/ff6_training_pairs.jsonl"
    )