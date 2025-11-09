#!/usr/bin/env python3
"""Check which items are missing recipes"""

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

# Collect all craftable items
all_items = []
for station_name, levels in workshop.get('stations', {}).items():
    for level_data in levels:
        for item_name in level_data.get('crafts', []):
            all_items.append((item_name, station_name, level_data.get('level', '')))

# Add upgrade items
base_items = [item for item, _, _ in all_items if item.endswith(' I')]
for base_item, station, level in all_items:
    if base_item.endswith(' I'):
        base_name = base_item[:-2].strip()
        for upgrade_level in ['II', 'III', 'IV']:
            upgrade_item = f'{base_name} {upgrade_level}'
            if not any(item == upgrade_item for item, _, _ in all_items):
                all_items.append((upgrade_item, station, level))

# Find items without recipes
items_without_recipes = []
items_with_recipes = []

for item, station, level in all_items:
    recipe = recipes.get(item, {})
    materials = recipe.get('required_materials', [])
    if materials:
        items_with_recipes.append((item, station, level, len(materials)))
    else:
        items_without_recipes.append((item, station, level))

print(f'Total craftable items: {len(all_items)}')
print(f'Items with recipes: {len(items_with_recipes)}')
print(f'Items without recipes: {len(items_without_recipes)}')
print(f'\n{"="*60}')
print('Items WITHOUT recipes (grouped by station):')
print(f'{"="*60}')

# Group by station
by_station = {}
for item, station, level in items_without_recipes:
    if station not in by_station:
        by_station[station] = []
    by_station[station].append((item, level))

for station in sorted(by_station.keys()):
    print(f'\n{station}:')
    for item, level in sorted(by_station[station]):
        print(f'  - {item} ({level})')

print(f'\n{"="*60}')
print('Items WITH recipes:')
print(f'{"="*60}')
for item, station, level, mat_count in sorted(items_with_recipes):
    print(f'  ✓ {item} ({station}, {level}) - {mat_count} materials')

