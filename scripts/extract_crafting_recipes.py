#!/usr/bin/env python3
"""
Extract crafting recipes from ARC Raiders Wiki
Only extracts base crafting recipes (not upgrades)
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os

BASE_URLS = [
    "https://arcraiders.wiki",
    "https://arc-raiders.fandom.com"
]

def extract_crafting_recipes():
    """Extract only crafting recipes (not upgrades)"""
    print("🔧 Extracting crafting recipes...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    workshop_file = os.path.join(project_root, 'data', 'workshop_level_ups.json')
    
    with open(workshop_file, 'r', encoding='utf-8') as f:
        workshop_data = json.load(f)
    
    craftable_items = {}
    for station_name, levels in workshop_data.get('stations', {}).items():
        for level_data in levels:
            level = level_data.get('level', '')
            for item_name in level_data.get('crafts', []):
                if item_name not in craftable_items:
                    craftable_items[item_name] = {
                        'station': station_name,
                        'level': level
                    }
    
    print(f"Found {len(craftable_items)} craftable items")
    
    recipes = {}
    processed_pages = set()
    
    # Process EACH item individually to ensure all are checked
    for item_name in sorted(craftable_items.keys()):
        # Generate URL variations for this specific item
        url_variations = []
        
        # Base variations
        url_variations.append(item_name.replace(' ', '_'))
        url_variations.append(item_name.replace(' ', '_').replace("'", "'"))
        
        # If item ends with " I", also try without it
        if item_name.endswith(' I'):
            base_name = item_name[:-2].strip()
            url_variations.insert(0, base_name.replace(' ', '_'))
        
        # Try each URL variation
        for wiki_name in url_variations:
            for base_url in BASE_URLS:
                url = f"{base_url}/wiki/{wiki_name}"
                if url in processed_pages:
                    continue
                
                try:
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        main_content = soup.find('div', class_='mw-parser-output')
                        if main_content:
                            tables = main_content.find_all('table')
                            for table in tables:
                                rows = table.find_all('tr')
                                if len(rows) < 2:
                                    continue
                                
                                headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]
                                headers_text = ' '.join(headers)
                                
                                # Check for crafting recipe tables (not upgrade)
                                is_upgrade_table = 'upgraded' in headers_text or ('upgrade' in headers_text and ('stats' in headers_text or 'perks' in headers_text))
                                is_recipe_table = 'recipe' in headers_text or 'craft' in headers_text or 'blueprint' in headers_text
                                
                                # Check if table contains upgrade items (II, III, IV) - skip those
                                has_upgrade_items = False
                                if is_recipe_table:
                                    for row in rows[1:3]:  # Check first few rows
                                        cells = row.find_all(['td', 'th'])
                                        if len(cells) > 4:
                                            result_text = cells[4].get_text().strip()
                                            if re.search(r'\s+(II|III|IV)$', result_text):
                                                has_upgrade_items = True
                                                break
                                
                                if is_recipe_table and not is_upgrade_table and not has_upgrade_items:
                                    for row in rows[1:]:
                                        cells = row.find_all(['td', 'th'])
                                        if len(cells) < 3:
                                            continue
                                        
                                        # Get recipe cell with <br> tags converted to newlines
                                        recipe_cell = cells[0].get_text(separator='\n').strip()
                                        
                                        # Find result item
                                        result_item = None
                                        if len(cells) > 4:
                                            result_item = cells[4].get_text().strip()
                                        elif len(cells) > 3:
                                            result_item = cells[3].get_text().strip()
                                        
                                        if not result_item:
                                            continue
                                        
                                        # Remove quantity prefix
                                        result_item = re.sub(r'^\d+\s*[x×]?\s*', '', result_item).strip()
                                        
                                        # Match to craftable items
                                        matching_items = []
                                        for craftable_item in craftable_items.keys():
                                            if craftable_item.lower() == result_item.lower():
                                                matching_items.append(craftable_item)
                                                break
                                        
                                        # Try base name matching
                                        if not matching_items:
                                            result_base = re.sub(r'\s+(I{1,3}|IV|V)$', '', result_item).strip().lower()
                                            if result_base:
                                                for craftable_item in craftable_items.keys():
                                                    item_base = re.sub(r'\s+(I{1,3}|IV|V)$', '', craftable_item).strip().lower()
                                                    if item_base == result_base:
                                                        matching_items.append(craftable_item)
                                        
                                        # Try partial matching
                                        if not matching_items:
                                            result_clean = result_item.lower().strip()
                                            for craftable_item in craftable_items.keys():
                                                item_clean = craftable_item.lower().strip()
                                                if result_clean == item_clean or (result_clean in item_clean and len(result_clean) > 3):
                                                    matching_items.append(craftable_item)
                                        
                                        if not matching_items:
                                            continue
                                        
                                        # Parse materials
                                        for matched_item in matching_items:
                                            if not recipes.get(matched_item, {}).get('required_materials'):
                                                materials = []
                                                # Normalize recipe text
                                                recipe_normalized = recipe_cell.replace('\n', ' ').replace('+', ' ').strip()
                                                recipe_normalized = re.sub(r'([A-Za-z])(\d+\s*[x×])', r'\1 \2', recipe_normalized)
                                                
                                                # Find all material patterns
                                                pattern = r'(\d+)\s*[x×]?\s*([A-Za-z][A-Za-z\s]*?)(?=\s*\d+\s*[x×]|\s*$|$)'
                                                matches = re.findall(pattern, recipe_normalized, re.IGNORECASE)
                                                
                                                if not matches:
                                                    match = re.match(r'(\d+)\s*[x×]?\s*(.+?)$', recipe_normalized, re.IGNORECASE)
                                                    if match:
                                                        matches = [match.groups()]
                                                
                                                for qty, mat in matches:
                                                    mat = mat.strip()
                                                    if not mat:
                                                        continue
                                                    # Skip base items (for upgrades)
                                                    if re.match(r'^[A-Za-z\s]+?\s+(I{1,3}|IV|V)$', mat):
                                                        continue
                                                    skip_keywords = ['gunsmith', 'workshop', 'level', 'blueprint', 'required', 'no', 'yes', 'upgrade', 'stats', 'perks']
                                                    if not any(kw in mat.lower() for kw in skip_keywords):
                                                        materials.append({"material": mat, "quantity": int(qty)})
                                                
                                                if materials:
                                                    recipes[matched_item] = {'required_materials': materials}
                                                    print(f"  ✓ {matched_item}: {len(materials)} materials")
                        
                        processed_pages.add(url)
                        time.sleep(0.3)
                        break
                except Exception as e:
                    continue
            
            if url in processed_pages:
                break
    
    # Merge with workshop data
    result = {}
    for item_name, item_info in craftable_items.items():
        result[item_name] = {
            'station': item_info['station'],
            'level': item_info['level'],
            'required_materials': recipes.get(item_name, {}).get('required_materials', [])
        }
    
    return result

def main():
    print("=" * 60)
    print("ARC Raiders - Crafting Recipes Extraction")
    print("=" * 60)
    
    recipes = extract_crafting_recipes()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_file = os.path.join(project_root, 'data', 'crafting_recipes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved {len(recipes)} recipes to {output_file}")
    
    import shutil
    shutil.copy(output_file, os.path.join(project_root, 'frontend', 'public', 'crafting_recipes.json'))
    print("✅ Copied to frontend/public/crafting_recipes.json")
    
    with_recipes = sum(1 for r in recipes.values() if r.get('required_materials'))
    print(f"\n{'='*60}")
    print(f"Summary: {with_recipes}/{len(recipes)} items have crafting recipes")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
