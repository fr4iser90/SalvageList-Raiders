#!/usr/bin/env python3
"""Create a checklist of items with and without recipes"""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Load craftable items
with open(os.path.join(project_root, 'data', 'workshop_level_ups.json'), 'r') as f:
    workshop = json.load(f)

# Load recipes
with open(os.path.join(project_root, 'data', 'crafting_recipes.json'), 'r') as f:
    recipes = json.load(f)

# Collect all craftable items grouped by station
all_items_by_station = {}
for station_name, levels in workshop.get('stations', {}).items():
    all_items_by_station[station_name] = []
    for level_data in levels:
        level = level_data.get('level', '')
        for item_name in level_data.get('crafts', []):
            all_items_by_station[station_name].append((item_name, level))

# Add upgrade items
for station_name in list(all_items_by_station.keys()):
    items = all_items_by_station[station_name]
    base_items = [item for item, _ in items if item.endswith(' I')]
    for base_item, level in items:
        if base_item.endswith(' I'):
            base_name = base_item[:-2].strip()
            for upgrade_level in ['II', 'III', 'IV']:
                upgrade_item = f'{base_name} {upgrade_level}'
                if not any(item == upgrade_item for item, _ in items):
                    all_items_by_station[station_name].append((upgrade_item, level))

# Create checklist
print("="*80)
print("CRAFTING RECIPES CHECKLIST")
print("="*80)
print()

total_with = 0
total_without = 0

for station in sorted(all_items_by_station.keys()):
    items = sorted(all_items_by_station[station])
    with_recipes = []
    without_recipes = []
    
    for item, level in items:
        recipe = recipes.get(item, {})
        materials = recipe.get('required_materials', [])
        if materials:
            with_recipes.append((item, level, len(materials)))
            total_with += 1
        else:
            without_recipes.append((item, level))
            total_without += 1
    
    print(f"{station}:")
    print(f"  ✅ WITH recipes: {len(with_recipes)}/{len(items)}")
    for item, level, mat_count in with_recipes:
        print(f"     ✓ {item:40} ({level:12}) - {mat_count} materials")
    
    if without_recipes:
        print(f"  ❌ WITHOUT recipes: {len(without_recipes)}/{len(items)}")
        for item, level in without_recipes:
            print(f"     ✗ {item:40} ({level:12})")
    print()

print("="*80)
print(f"SUMMARY: {total_with} with recipes, {total_without} without recipes")
print(f"Total: {total_with + total_without} items")
print("="*80)

# Save to file
output_file = os.path.join(project_root, 'docs', 'RECIPE_CHECKLIST.md')
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Crafting Recipes Checklist\n\n")
    f.write(f"**Status:** {total_with}/{total_with + total_without} items have recipes ({total_with*100//(total_with+total_without)}%)\n\n")
    f.write("---\n\n")
    
    for station in sorted(all_items_by_station.keys()):
        items = sorted(all_items_by_station[station])
        with_recipes = []
        without_recipes = []
        
        for item, level in items:
            recipe = recipes.get(item, {})
            materials = recipe.get('required_materials', [])
            if materials:
                with_recipes.append((item, level, len(materials)))
            else:
                without_recipes.append((item, level))
        
        f.write(f"## {station}\n\n")
        f.write(f"**Status:** {len(with_recipes)}/{len(items)} items have recipes\n\n")
        
        if with_recipes:
            f.write("### ✅ Items WITH recipes:\n\n")
            for item, level, mat_count in with_recipes:
                f.write(f"- [x] **{item}** ({level}) - {mat_count} materials\n")
            f.write("\n")
        
        if without_recipes:
            f.write("### ❌ Items WITHOUT recipes:\n\n")
            for item, level in without_recipes:
                f.write(f"- [ ] **{item}** ({level})\n")
            f.write("\n")
        
        f.write("---\n\n")

print(f"\n✅ Checklist saved to: {output_file}")

