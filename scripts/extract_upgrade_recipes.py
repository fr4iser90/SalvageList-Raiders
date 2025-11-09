#!/usr/bin/env python3
"""
Extract upgrade recipes from ARC Raiders Wiki
Only extracts upgrade recipes (II, III, IV)
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

def extract_upgrade_recipes():
    """Extract only upgrade recipes"""
    print("⬆️  Extracting upgrade recipes...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    workshop_file = os.path.join(project_root, 'data', 'workshop_level_ups.json')
    
    with open(workshop_file, 'r', encoding='utf-8') as f:
        workshop_data = json.load(f)
    
    # Collect all items including upgrades
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
    
    # Add upgrade items (II, III, IV)
    base_items = [item for item in craftable_items.keys() if item.endswith(' I')]
    for base_item in base_items:
        base_name = base_item[:-2].strip()
        for upgrade_level in ['II', 'III', 'IV']:
            upgrade_item = f"{base_name} {upgrade_level}"
            if upgrade_item not in craftable_items:
                base_info = craftable_items[base_item]
                craftable_items[upgrade_item] = {
                    'station': base_info['station'],
                    'level': base_info['level']
                }
    
    print(f"Found {len(craftable_items)} items (including upgrades)")
    
    recipes = {}
    processed_pages = set()
    
    # Group items by base name
    base_item_names = set()
    items_by_base = {}
    for item_name in craftable_items.keys():
        base_match = re.match(r'^(.+?)\s+(I{1,3}|IV|V)$', item_name)
        if base_match:
            base_name = base_match.group(1).strip()
            base_item_names.add(base_name)
            if base_name not in items_by_base:
                items_by_base[base_name] = []
            items_by_base[base_name].append(item_name)
        else:
            base_item_names.add(item_name)
            if item_name not in items_by_base:
                items_by_base[item_name] = []
            items_by_base[item_name].append(item_name)
    
    # Process each base name
    for base_name in sorted(base_item_names):
        related_items = items_by_base.get(base_name, [base_name])
        url_variations = []
        
        # Generate URL variations
        url_variations.append(base_name.replace(' ', '_'))
        url_variations.append(base_name.replace(' ', '_').replace("'", "'"))
        
        if base_name.endswith(' I'):
            base_without_i = base_name[:-2].strip()
            url_variations.insert(0, base_without_i.replace(' ', '_'))
        
        for item in related_items:
            item_wiki = item.replace(' ', '_').replace("'", "'")
            if item_wiki not in url_variations:
                url_variations.append(item_wiki)
        
        # Remove duplicates
        seen = set()
        url_variations = [x for x in url_variations if not (x in seen or seen.add(x))]
        
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
                                
                                # Check for upgrade recipe tables
                                # Upgrade tables can have "upgrade perks" or just "upgrade" in headers
                                # Also check if result items are II, III, IV
                                is_upgrade_table = 'upgraded' in headers_text or ('upgrade' in headers_text and ('stats' in headers_text or 'perks' in headers_text))
                                is_recipe_table = 'recipe' in headers_text or 'craft' in headers_text
                                
                                # Process upgrade tables OR tables that might contain upgrade recipes
                                # Check if table contains II/III/IV items in result column
                                has_upgrade_items = False
                                if is_recipe_table:
                                    for row in rows[1:3]:  # Check first few rows
                                        cells = row.find_all(['td', 'th'])
                                        if len(cells) > 4:
                                            result_text = cells[4].get_text().strip()
                                            if re.search(r'\s+(II|III|IV)$', result_text):
                                                has_upgrade_items = True
                                                break
                                
                                if is_recipe_table and (is_upgrade_table or 'upgrade' in headers_text or has_upgrade_items):
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
                                        
                                        # Match to upgrade items (II, III, IV)
                                        matching_items = []
                                        for item in craftable_items.keys():
                                            if item.lower() == result_item.lower():
                                                matching_items.append(item)
                                                break
                                        
                                        if not matching_items:
                                            result_base = re.sub(r'\s+(I{1,3}|IV|V)$', '', result_item).strip().lower()
                                            if result_base:
                                                for item in craftable_items.keys():
                                                    item_base = re.sub(r'\s+(I{1,3}|IV|V)$', '', item).strip().lower()
                                                    if item_base == result_base and re.search(r'\s+(II|III|IV)$', item):
                                                        result_level_match = re.search(r'\s+(II|III|IV)$', result_item)
                                                        item_level_match = re.search(r'\s+(II|III|IV)$', item)
                                                        if result_level_match and item_level_match:
                                                            if result_level_match.group(1) == item_level_match.group(1):
                                                                matching_items.append(item)
                                                        elif not result_level_match:
                                                            matching_items.append(item)
                                        
                                        for item_name in matching_items:
                                            if re.search(r'\s+(II|III|IV)$', item_name):
                                                materials = []
                                                # Normalize recipe text
                                                recipe_text = recipe_cell.replace('\n', ' ').replace('+', ' ').strip()
                                                recipe_text = re.sub(r'([A-Za-z])(\d+\s*[x×])', r'\1 \2', recipe_text)
                                                
                                                # Check for base item first
                                                base_item_match = re.match(r'^([A-Za-z\s]+?)\s+(I{1,3}|IV|V)(.*)$', recipe_text)
                                                if base_item_match:
                                                    base_item = base_item_match.group(1).strip() + ' ' + base_item_match.group(2)
                                                    if base_item.lower() != result_item.lower():
                                                        materials.append({"material": base_item, "quantity": 1})
                                                    # Continue with remaining text
                                                    remaining = base_item_match.group(3).strip()
                                                    if remaining:
                                                        recipe_text = remaining
                                                
                                                # Find all material patterns
                                                pattern = r'(\d+)\s*[x×]?\s*([A-Za-z][A-Za-z\s]*?)(?=\s*\d+\s*[x×]|\s*$|$)'
                                                matches = re.findall(pattern, recipe_text, re.IGNORECASE)
                                                
                                                if not matches:
                                                    match = re.match(r'(\d+)\s*[x×]?\s*(.+?)$', recipe_text, re.IGNORECASE)
                                                    if match:
                                                        matches = [match.groups()]
                                                
                                                for qty, mat in matches:
                                                    mat = mat.strip()
                                                    if not mat:
                                                        continue
                                                    skip_keywords = ['gunsmith', 'workshop', 'level', 'upgrade', 'stats', 'perks']
                                                    if not any(kw in mat.lower() for kw in skip_keywords):
                                                        materials.append({"material": mat, "quantity": int(qty)})
                                                
                                                if materials:
                                                    recipe_data = {'required_materials': materials, 'is_upgrade': True}
                                                    base_item = next((m['material'] for m in materials if re.search(r'\s+(I{1,3}|IV|V)$', m.get('material', ''))), None)
                                                    if base_item:
                                                        recipe_data['upgrade_from'] = base_item
                                                    recipes[item_name] = recipe_data
                                                    print(f"  ✓ {item_name}: {len(materials)} materials")
                        
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
        if re.search(r'\s+(II|III|IV)$', item_name):
            recipe_data = recipes.get(item_name, {})
            result[item_name] = {
                'station': item_info['station'],
                'level': item_info['level'],
                'required_materials': recipe_data.get('required_materials', [])
            }
            if 'upgrade_from' in recipe_data:
                result[item_name]['upgrade_from'] = recipe_data['upgrade_from']
    
    return result

def main():
    print("=" * 60)
    print("ARC Raiders - Upgrade Recipes Extraction")
    print("=" * 60)
    
    recipes = extract_upgrade_recipes()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_file = os.path.join(project_root, 'data', 'upgrade_recipes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved {len(recipes)} recipes to {output_file}")
    
    import shutil
    shutil.copy(output_file, os.path.join(project_root, 'frontend', 'public', 'upgrade_recipes.json'))
    print("✅ Copied to frontend/public/upgrade_recipes.json")
    
    with_recipes = sum(1 for r in recipes.values() if r.get('required_materials'))
    print(f"\n{'='*60}")
    print(f"Summary: {with_recipes}/{len(recipes)} items have upgrade recipes")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
