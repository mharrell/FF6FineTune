import requests
import json
import time
import os

BASE_URL = "https://finalfantasy.fandom.com/api.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

VERSION_KEYWORDS = {
    "snes": ["snes", "super nintendo", "ff3", "woolsey", "original version"],
    "ps1": ["ps1", "playstation", "psx"],
    "gba": ["gba", "game boy advance", "advance version"],
    "ios": ["ios", "android", "mobile version"],
    "steam": ["steam", "pc version", "old steam"],
    "pixel_remaster": ["pixel remaster", "pr version", "2022"]
}

FF6_PAGES = [

    # Main
    "Final_Fantasy_VI",

    # Characters
    "Terra_Branford",
    "Locke_Cole",
    "Edgar_Roni_Figaro",
    "Sabin_Rene_Figaro",
    "Celes_Chere",
    "Cyan_Garamonde",
    "Shadow_(Final_Fantasy_VI)",
    "Gau",
    "Setzer_Gabbiani",
    "Mog_(Final_Fantasy_VI)",
    "Strago_Magus",
    "Relm_Arrowny",
    "Umaro",
    "Gogo_(Final_Fantasy_VI)",
    "Kefka_Palazzo",

    # Abilities & Commands
    "Blitz_(Final_Fantasy_VI)",
    "Lore_(Final_Fantasy_VI)",
    "Sketch",
    "Dance_(Final_Fantasy_VI)",
    "Steal_(Final_Fantasy_VI)",
    "Rage_(Final_Fantasy_VI_command)",
    "Magic_(Final_Fantasy_VI_command)",
    "Tools_(command)",
    "Desperation_Attack",
    "Magitek_(command)",
    "Trance_(Final_Fantasy_VI)",
    "Bushido_(Final_Fantasy_VI)",

    # Espers & Magicite
    "Esper_(Final_Fantasy_VI)",
    "Magicite_(Final_Fantasy_VI)",
    "Carbuncle_(Final_Fantasy_VI)",
    "Catoblepas_(Final_Fantasy_VI)",
    "Zona_Seeker_(Final_Fantasy_VI)",
    "Alexander_(Final_Fantasy_VI)",
    "Crusader_(summon)",
    "Ragnarok_(Final_Fantasy_VI_summon)",
    "Fenrir_(Final_Fantasy_VI)",
    "Golem_(Final_Fantasy_VI)",
    "Quetzalli_(Final_Fantasy_VI)"

    # Individual Espers
    "Ramuh_(Final_Fantasy_VI)",
    "Ifrit_(Final_Fantasy_VI)",
    "Shiva_(Final_Fantasy_VI)",
    "Kirin_(Final_Fantasy_VI)",
    "Siren_(Final_Fantasy_VI)",
    "Cait_Sith_(Final_Fantasy_VI)",
    "Bismarck_(Final_Fantasy_VI)",
    "Lakshmi_(Final_Fantasy_VI)",
    "Valigarmanda_(Final_Fantasy_VI)",
    "Phantom_(Final_Fantasy_VI)",
    "Carbunkl_(Final_Fantasy_VI)",
    "Maduin_(Final_Fantasy_VI)",
    "Shoat_(Final_Fantasy_VI)",
    "Unicorn_(Final_Fantasy_VI)",
    "Zone_Seeker_(Final_Fantasy_VI)",
    "Alexandr_(Final_Fantasy_VI)",
    "Crusader_(Final_Fantasy_VI)",
    "Ragnarok_(Final_Fantasy_VI)",
    "Bahamut_(Final_Fantasy_VI)",
    "Odin_(Final_Fantasy_VI)",
    "Raiden_(Final_Fantasy_VI)",
    "Phoenix_(Final_Fantasy_VI)",
    "Leviathan_(Final_Fantasy_VI)",
    "Gilgamesh_(Final_Fantasy_VI)",
    "Gigantuar_(Final_Fantasy_VI)",
    "Diabolos_(Final_Fantasy_VI)",

    # Equipment & Items
    "Relic_(Final_Fantasy_VI)",
    "Final_Fantasy_VI_weapons",
    "Final_Fantasy_VI_armor",
    "Final_Fantasy_VI_items",

    # Acquisition & Shops
    "Dragon's_Neck_Coliseum",
    "Auction_House_(Final_Fantasy_VI)",

    # Locations
    "Narshe",
    "Figaro_Castle",
    "South_Figaro",
    "Vector_(Final_Fantasy_VI)",
    "Zozo_(Final_Fantasy_VI)",
    "Jidoor",
    "Thamasa",
    "Mobliz",
    "Kohlingen",
    "Kefka's_Tower",
    "Dragons'_Den",
    "Soul_Shrine",
    "Magitek_Research_Facility_(Final_Fantasy_VI)",
    "Phantom_Train_(Final_Fantasy_VI)",
    "Opera_House_(Final_Fantasy_VI)",
    "Veldt",
    "Doma_Castle_(Final_Fantasy_VI)",
    "Vector",
    # Battle System
    "Active_Time_Battle",
    "Final_Fantasy_VI_battle_system",

    # Story & World
    "Returners",
    "Gestahlian_Empire",
    "World_of_Balance",
    "World_of_Ruin_(Final_Fantasy_VI)",
    "Floating_Continent_(Final_Fantasy_VI)",
    "War_of_the_Magi_(Final_Fantasy_VI)",
    "Warring_Triad_(Final_Fantasy_VI)",
    "Magitek",

    # Enemies & Bestiary
    "Final_Fantasy_VI_enemies",
    "Bestiary_(Final_Fantasy_VI)",
]

def detect_versions(text):
    text_lower = text.lower()
    found_versions = []
    for version, keywords in VERSION_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found_versions.append(version)
    return found_versions if found_versions else ["all_versions"]

def scrape_page_api(title):
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2"
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", [])
        if not pages:
            return None

        page = pages[0]
        if "missing" in page:
            print(f"  -> Page not found: {title}")
            return None

        content = page.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("content", "")

        if not content:
            return None

        # Split into sections by == headings ==
        sections = []
        current_heading = "Introduction"
        current_content = ""

        for line in content.split("\n"):
            if line.startswith("==") and not line.startswith("==="):
                if current_content.strip():
                    sections.append({
                        "heading": current_heading,
                        "content": current_content.strip(),
                        "versions": detect_versions(current_content)
                    })
                current_heading = line.replace("=", "").strip()
                current_content = ""
            else:
                current_content += " " + line

        # Last section
        if current_content.strip():
            sections.append({
                "heading": current_heading,
                "content": current_content.strip(),
                "versions": detect_versions(current_content)
            })

        return {
            "title": title,
            "url": f"https://finalfantasy.fandom.com/wiki/{title}",
            "sections": sections
        }

    except Exception as e:
        print(f"Error scraping {title}: {e}")
        return None


def scrape_all():
    os.makedirs("data/raw", exist_ok=True)
    all_data = []

    for i, page in enumerate(FF6_PAGES):
        print(f"Scraping ({i+1}/{len(FF6_PAGES)}): {page}")
        data = scrape_page_api(page)
        if data:
            all_data.append(data)
            print(f"  -> Got {len(data['sections'])} sections for '{data['title']}'")
        else:
            print(f"  -> Failed or not found")

        time.sleep(1)

    output_path = "data/raw/ff6_wiki_raw.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Scraped {len(all_data)} pages.")
    print(f"Saved to {output_path}")
    return all_data


if __name__ == "__main__":
    scrape_all()