#!/usr/bin/env python3
"""Test specific items to see if they have recipes in the wiki"""

import requests
from bs4 import BeautifulSoup
import re

BASE_URLS = [
    "https://arc-raiders.fandom.com",
    "https://arcraiders.wiki"
]

# Items to test
test_items = [
    "Rattler I",
    "Arpeggio I", 
    "Renegade I",
    "Stitcher I",
    "Angled Grip I",
    "Compensator I",
    "Muzzle Brake I",
    "Vertical Grip I",
    "Stable Stock I",
    "Extended Light Mag I",
    "Shotgun Choke I"
]

def check_item(item_name):
    """Check if item has recipe on wiki"""
    # Try different URL variations
    wiki_name_variations = [
        item_name.replace(' ', '_').replace('.', '').replace("'", "'"),
        item_name.replace(' ', '_').replace('.', ''),
        item_name.replace(' ', '_'),
        item_name
    ]
    
    # Remove " I" for base name
    if item_name.endswith(' I'):
        base_name = item_name[:-2].strip()
        wiki_name_variations.insert(0, base_name.replace(' ', '_'))
    
    for wiki_name in wiki_name_variations:
        for base_url in BASE_URLS:
            url = f"{base_url}/wiki/{wiki_name}"
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    main_content = soup.find('div', class_='mw-parser-output')
                    
                    if main_content:
                        # Check for recipe sections
                        text = main_content.get_text().lower()
                        has_recipe = any(keyword in text for keyword in ['recipe', 'craft', 'required material', 'materials to craft'])
                        
                        # Check for tables with recipe headers
                        tables = main_content.find_all('table')
                        recipe_tables = []
                        for table in tables:
                            rows = table.find_all('tr')
                            if len(rows) > 0:
                                headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]
                                headers_text = ' '.join(headers)
                                if 'recipe' in headers_text or ('material' in headers_text and 'craft' in headers_text):
                                    recipe_tables.append(headers_text[:80])
                        
                        if has_recipe or recipe_tables:
                            print(f"  ✓ {item_name}: Found recipe info at {url}")
                            if recipe_tables:
                                print(f"    Tables: {recipe_tables[0]}")
                            return True
                        
            except Exception as e:
                continue
    
    print(f"  ✗ {item_name}: No recipe found")
    return False

print("Testing items for recipes...")
print("="*60)

found = 0
for item in test_items:
    if check_item(item):
        found += 1
    import time
    time.sleep(0.5)

print(f"\n{'='*60}")
print(f"Found recipes for {found}/{len(test_items)} items")

