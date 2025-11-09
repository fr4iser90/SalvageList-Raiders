#!/usr/bin/env python3
"""Test more missing items"""

import requests
from bs4 import BeautifulSoup

BASE_URLS = ["https://arc-raiders.fandom.com", "https://arcraiders.wiki"]

test_items = [
    "Angled Grip I",
    "Compensator I", 
    "Muzzle Brake I",
    "Vertical Grip I",
    "Stable Stock I",
    "Extended Light Mag I",
    "Shotgun Choke I",
    "Arpeggio I",
    "Gas Grenade",
    "Blaze Grenade"
]

def check_item(item_name):
    wiki_name = item_name.replace(' ', '_').replace('.', '').replace("'", "'")
    
    # Try without " I"
    if item_name.endswith(' I'):
        base_name = item_name[:-2].strip().replace(' ', '_')
        variations = [base_name, wiki_name]
    else:
        variations = [wiki_name]
    
    for wiki_name_var in variations:
        for base_url in BASE_URLS:
            url = f"{base_url}/wiki/{wiki_name_var}"
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    main_content = soup.find('div', class_='mw-parser-output')
                    if main_content:
                        text = main_content.get_text().lower()
                        if 'recipe' in text or 'craft' in text:
                            print(f"  ✓ {item_name}: {url}")
                            return True
            except:
                continue
    print(f"  ✗ {item_name}")
    return False

for item in test_items:
    check_item(item)
    import time
    time.sleep(0.3)

