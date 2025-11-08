#!/usr/bin/env python3
"""
Extract all data: Traders, Workshop, Projects
ONLY DATA EXTRACTION - NO UI CHANGES
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://arc-raiders.fandom.com"

def extract_trader_data():
    """Extract trader information"""
    print("📦 Extracting Trader Data...")
    
    TRADERS = [
        {"name": "Celeste", "url": "Celeste", "category": "Basic Materials"},
        {"name": "Tian Wen", "url": "Tian_Wen", "category": "Weapons & Ammo"},
        {"name": "Apollo", "url": "Apollo", "category": "Grenades & Gadgets"},
        {"name": "Shani", "url": "Shani", "category": "Security"},
        {"name": "Lance", "url": "Lance", "category": "Medical, Shields & Augments"},
    ]
    
    materials_info = []
    
    for trader in TRADERS:
        url = f"{BASE_URL}/wiki/{trader['url']}"
        print(f"  Fetching {trader['name']}...")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            main_content = soup.find('div', class_='mw-parser-output')
            if not main_content:
                continue
            
            tables = main_content.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 2:
                    continue
                
                header_row = rows[0]
                headers = [th.get_text().strip().lower() for th in header_row.find_all(['th', 'td'])]
                headers_text = ' '.join(headers)
                
                # Check if this is a trader table
                if 'item' in headers_text or 'required resources' in headers_text or 'material' in headers_text or 'price' in headers_text:
                    # Find column indices
                    item_col = None
                    price_col = None
                    material_col = None
                    
                    for i, header in enumerate(headers):
                        header_lower = header.lower()
                        if 'item' in header_lower:
                            item_col = i
                        elif 'required resources' in header_lower or 'price' in header_lower or 'cost' in header_lower:
                            price_col = i
                        elif 'material' in header_lower:
                            material_col = i
                    
                    # Use item_col or material_col for material
                    material_col_idx = item_col if item_col is not None else material_col
                    
                    for row in rows[1:]:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) < 2:
                            continue
                        
                        material = ""
                        price = ""
                        
                        # Extract material from correct column
                        if material_col_idx is not None and material_col_idx < len(cells):
                            material = cells[material_col_idx].get_text().strip()
                        
                        # Extract price from correct column
                        if price_col is not None and price_col < len(cells):
                            price = cells[price_col].get_text().strip()
                        
                        # Clean up material name
                        if material:
                            material = material.replace('\n', ' ').strip()
                            # Remove common prefixes/suffixes
                            material = re.sub(r'^x\d+\s*', '', material, flags=re.IGNORECASE)
                            material = re.sub(r'\s*x\d+$', '', material, flags=re.IGNORECASE)
                        
                        # Skip if material is a price (starts with $) or invalid
                        if material and material.startswith('$'):
                            continue
                        
                        # Skip header-like values
                        if material and material.lower() not in ['required resources', 'item', 'material', 'price', 'cost', 'level requirement', '']:
                            # Check if already exists
                            existing = next((m for m in materials_info if m.get('material') == material), None)
                            if existing:
                                existing['trader'] = {
                                    "available": True,
                                    "trader_name": trader['name'],
                                    "price": price or "Unknown",
                                    "frequency": "Daily"
                                }
                            else:
                                materials_info.append({
                                    "material": material,
                                    "trader": {
                                        "available": True,
                                        "trader_name": trader['name'],
                                        "price": price or "Unknown",
                                        "frequency": "Daily"
                                    }
                                })
            
            time.sleep(2)
        except Exception as e:
            print(f"  Error: {e}")
    
    return materials_info

def extract_workshop_data():
    """Extract workshop level-up data"""
    print("\n🔨 Extracting Workshop Data...")
    
    url = f"{BASE_URL}/wiki/Workshop"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('div', class_='mw-parser-output')
        if not main_content:
            return {}
        
        stations = {}
        station_names = ["Workbench", "Gunsmith", "Gear Bench", "Explosives Station", 
                        "Medical Lab", "Utility Station", "Refiner", "Scrappy the Rooster"]
        
        for station_name in station_names:
            # Find section
            for h in main_content.find_all(['h2', 'h3']):
                if station_name.lower() in h.get_text().lower():
                    station_data = []
                    current = h.find_next_sibling()
                    
                    while current and current.name not in ['h2', 'h3']:
                        if current.name == 'table':
                            rows = current.find_all('tr')
                            if len(rows) >= 2:
                                headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]
                                
                                for row in rows[1:]:
                                    cells = row.find_all(['td', 'th'])
                                    if len(cells) >= 2:
                                        level = ""
                                        required_resources = []
                                        crafts = []
                                        
                                        for i, cell in enumerate(cells):
                                            if i < len(headers):
                                                header = headers[i]
                                                text = cell.get_text().strip()
                                                
                                                if 'level' in header:
                                                    level = text
                                                elif 'required' in header or 'resource' in header:
                                                    # Parse resources
                                                    pattern = r'(\d+)\s*[x×]\s*([^,\n]+?)(?=\s*\d+\s*[x×]|,|\n|$)'
                                                    matches = re.findall(pattern, text, re.IGNORECASE)
                                                    for qty, mat in matches:
                                                        required_resources.append({
                                                            "material": mat.strip(),
                                                            "quantity": int(qty)
                                                        })
                                                elif 'craft' in header:
                                                    crafts = [c.strip() for c in text.split('\n') if c.strip()]
                                        
                                        if level:
                                            station_data.append({
                                                "level": level,
                                                "required_resources": required_resources,
                                                "crafts": crafts
                                            })
                        current = current.find_next_sibling()
                    
                    if station_data:
                        stations[station_name] = station_data
                    break
        
        return {"stations": stations}
    except Exception as e:
        print(f"  Error: {e}")
        return {}

def extract_projects_data():
    """Extract expedition projects data"""
    print("\n📋 Extracting Projects Data...")
    
    url = f"{BASE_URL}/wiki/Expedition_Projects"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"  Status: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('div', class_='mw-parser-output')
        if not main_content:
            return []
        
        projects = []
        tables = main_content.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue
            
            headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]
            
            if 'caravan build' in str(headers) or 'required materials' in str(headers):
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        project_name = ""
                        description = ""
                        required_materials = []
                        
                        for i, cell in enumerate(cells):
                            if i < len(headers):
                                header = headers[i]
                                text = cell.get_text().strip()
                                
                                if 'caravan build' in header or 'name' in header:
                                    project_name = text
                                elif 'description' in header:
                                    description = text
                                elif 'required materials' in header or 'materials' in header:
                                    # Parse materials
                                    pattern = r'(\d+)\s*[x×]\s*([^,\n]+?)(?=\s*\d+\s*[x×]|,|\n|$)'
                                    matches = re.findall(pattern, text, re.IGNORECASE)
                                    for qty, mat in matches:
                                        required_materials.append({
                                            "material": mat.strip(),
                                            "quantity": int(qty)
                                        })
                        
                        if project_name and project_name.lower() not in ['none', '']:
                            projects.append({
                                "name": project_name,
                                "description": description,
                                "required_materials": required_materials
                            })
        
        return projects
    except Exception as e:
        print(f"  Error: {e}")
        return []

def main():
    print("=" * 60)
    print("ARC Raiders - Data Extraction")
    print("=" * 60)
    
    # Extract all data
    materials_info = extract_trader_data()
    workshop_data = extract_workshop_data()
    projects_data = extract_projects_data()
    
    # Save materials-info.json
    with open('materials-info.json', 'w', encoding='utf-8') as f:
        json.dump(materials_info, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved {len(materials_info)} materials to materials-info.json")
    
    # Save workshop_level_ups.json
    with open('workshop_level_ups.json', 'w', encoding='utf-8') as f:
        json.dump(workshop_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved workshop data to workshop_level_ups.json")
    
    # Save expedition_projects.json
    with open('expedition_projects.json', 'w', encoding='utf-8') as f:
        json.dump(projects_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(projects_data)} projects to expedition_projects.json")
    
    # Copy to frontend/public
    import shutil
    shutil.copy('materials-info.json', 'frontend/public/materials-info.json')
    shutil.copy('workshop_level_ups.json', 'frontend/public/workshop_level_ups.json')
    shutil.copy('expedition_projects.json', 'frontend/public/expedition_projects.json')
    print("\n✅ All data files copied to frontend/public/")
    
    print("\n" + "=" * 60)
    print("✅ Data extraction complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

