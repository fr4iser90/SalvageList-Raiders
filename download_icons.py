#!/usr/bin/env python3
"""
Download icons for ARC Raiders items from the wiki.
Updates items.json with downloaded icon paths or keeps original URLs.
"""

import json
import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, quote
import time
from bs4 import BeautifulSoup

# Configuration
ITEMS_JSON = "items.json"
ICONS_DIR = "frontend/public/icons"
DELAY_BETWEEN_REQUESTS = 0.5  # Be nice to the server

def sanitize_filename(name):
    """Convert item name to safe filename."""
    # Replace spaces and special chars with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name.lower()

def get_image_extension(url):
    """Extract file extension from URL."""
    parsed = urlparse(url)
    path = parsed.path
    # Check for common image extensions
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        if ext in path.lower():
            return ext
    return '.png'  # Default

def download_image(url, filepath):
    """Download image from URL to filepath."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            print(f"  ⚠️  Warning: {url} doesn't appear to be an image (Content-Type: {content_type})")
            return False
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error downloading {url}: {e}")
        return False

# Cache for the Items page to avoid fetching it multiple times
_items_page_cache = None

def get_items_page_cache():
    """Fetch and cache the Items wiki page."""
    global _items_page_cache
    if _items_page_cache is None:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get('https://arc-raiders.fandom.com/wiki/Items', headers=headers, timeout=15)
            response.raise_for_status()
            _items_page_cache = BeautifulSoup(response.content, 'html.parser')
            print("  📚 Loaded Items wiki page cache")
        except Exception as e:
            print(f"  ⚠️  Could not load Items page: {e}")
            _items_page_cache = False
    return _items_page_cache

def find_image_in_items_page(item_name):
    """Find image URL from the Items wiki page."""
    soup = get_items_page_cache()
    if not soup:
        return None
    
    # Convert item name to match wiki format (spaces to underscores, special chars)
    wiki_name = item_name.replace(' ', '_')
    
    # Try to find the item in the table
    # Look for links or cells containing the item name
    tables = soup.find_all('table')
    if not tables:
        return None
    
    # Try each table
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Item name is in the second cell (index 1), image link is in first cell (index 0)
                name_cell_text = cells[1].get_text().strip()
                
                # Check for exact match or wiki name match
                if name_cell_text == item_name or name_cell_text == wiki_name:
                    # Find the image link in the first cell
                    first_cell = cells[0]
                    link = first_cell.find('a')
                    
                    if link:
                        # The href contains the image URL!
                        href = link.get('href')
                        if href and 'static.wikia.nocookie.net' in href:
                            # Remove query parameters and scale-to-width
                            if '?' in href:
                                href = href.split('?')[0]
                            if '/scale-to-width' in href:
                                href = href.split('/scale-to-width')[0]
                            return href
                    
                    # Fallback: try to find img tag
                    img = row.find('img')
                    if img:
                        # Try data-image-key to find the image elsewhere on the page
                        img_key = img.get('data-image-key')
                        if img_key:
                            # Search for this image key in the page to get the full URL
                            all_imgs = soup.find_all('img', {'data-image-key': img_key})
                            for test_img in all_imgs:
                                test_src = test_img.get('src')
                                if test_src and 'static.wikia.nocookie.net' in test_src:
                                    if '/scale-to-width' in test_src:
                                        test_src = test_src.split('/scale-to-width')[0]
                                    if '?' in test_src:
                                        test_src = test_src.split('?')[0]
                                    return test_src
    
    return None

def find_wiki_image_url(item_name, wiki_url=None):
    """Try to find the image URL from the wiki page."""
    # First, try the Items page (most items are there)
    image_url = find_image_in_items_page(item_name)
    if image_url:
        return image_url
    
    # If not found, try individual wiki page
    if not wiki_url:
        # Convert item name to wiki URL format
        wiki_name = item_name.replace(' ', '_')
        wiki_url = f"https://arc-raiders.fandom.com/wiki/{quote(wiki_name)}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(wiki_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the infobox image
        infobox = soup.find('aside', class_='portable-infobox')
        if infobox:
            img = infobox.find('img')
            if img and img.get('src'):
                # Get full resolution image
                src = img.get('src')
                # Remove scale-to-width parameter to get full size
                if '/scale-to-width/' in src:
                    src = src.split('/scale-to-width/')[0]
                # Or use data-src if available (lazy loading)
                if img.get('data-src'):
                    src = img.get('data-src')
                    if '/scale-to-width/' in src:
                        src = src.split('/scale-to-width/')[0]
                return src
        
        # Fallback: try to find any image in the article
        img = soup.find('img', {'data-image-key': True})
        if img:
            src = img.get('src') or img.get('data-src')
            if src and 'static.wikia.nocookie.net' in src:
                if '/scale-to-width/' in src:
                    src = src.split('/scale-to-width/')[0]
                return src
        
    except requests.exceptions.RequestException as e:
        # Don't print error for 404s (item doesn't have own page)
        if '404' not in str(e):
            print(f"  ⚠️  Could not fetch wiki page: {e}")
    except Exception as e:
        print(f"  ⚠️  Error parsing wiki page: {e}")
    
    return None

def process_items():
    """Process items.json and download missing icons."""
    # Create icons directory
    os.makedirs(ICONS_DIR, exist_ok=True)
    
    # Load items
    print(f"Loading {ITEMS_JSON}...")
    with open(ITEMS_JSON, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    print(f"Found {len(items)} items")
    
    downloaded = 0
    skipped = 0
    failed = 0
    updated = 0
    
    for i, item in enumerate(items, 1):
        name = item.get('name', 'Unknown')
        current_image = item.get('image', '')
        wiki_url = item.get('url', None)
        
        print(f"\n[{i}/{len(items)}] {name}")
        
        # Generate local filename
        safe_name = sanitize_filename(name)
        local_filename = f"{safe_name}.png"
        local_path = os.path.join(ICONS_DIR, local_filename)
        relative_path = f"/icons/{local_filename}"
        
        # If already using local path, skip
        if current_image.startswith('/icons/') or current_image.startswith('icons/'):
            print(f"  ✓ Already using local icon: {current_image}")
            continue
        
        # If it's a placeholder, try to find the image from wiki
        if current_image.startswith('data:'):
            print(f"  🔍 Placeholder detected, searching wiki...")
            
            # Check if already downloaded
            if os.path.exists(local_path):
                print(f"  ✓ Icon already exists: {relative_path}")
                item['image'] = relative_path
                updated += 1
                continue
            
            # Try to find image URL from wiki
            image_url = find_wiki_image_url(name, wiki_url)
            
            if image_url:
                print(f"  📥 Found image URL: {image_url}")
                if download_image(image_url, local_path):
                    item['image'] = relative_path
                    downloaded += 1
                    updated += 1
                    print(f"  ✅ Saved to {relative_path}")
                else:
                    failed += 1
                    print(f"  ⚠️  Download failed, keeping placeholder")
            else:
                print(f"  ⚠️  Could not find image URL, skipping")
                skipped += 1
            
            # Be nice to the server
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue
        
        # If it's a URL, try to download it
        if current_image.startswith('http'):
            # Generate local filename
            safe_name = sanitize_filename(name)
            ext = get_image_extension(current_image)
            local_filename = f"{safe_name}{ext}"
            local_path = os.path.join(ICONS_DIR, local_filename)
            relative_path = f"/icons/{local_filename}"
            
            # Check if already downloaded
            if os.path.exists(local_path):
                print(f"  ✓ Icon already exists: {relative_path}")
                # Update JSON to use local path if not already
                if item['image'] != relative_path:
                    item['image'] = relative_path
                    updated += 1
                continue
            
            # Download the image
            print(f"  📥 Downloading from {current_image}")
            if download_image(current_image, local_path):
                item['image'] = relative_path
                downloaded += 1
                updated += 1
                print(f"  ✅ Saved to {relative_path}")
            else:
                failed += 1
                # Keep original URL if download fails
                print(f"  ⚠️  Keeping original URL")
            
            # Be nice to the server
            time.sleep(DELAY_BETWEEN_REQUESTS)
        else:
            print(f"  ⚠️  Unknown image format: {current_image}")
            skipped += 1
    
    # Save updated items.json
    if updated > 0:
        print(f"\n💾 Saving updated {ITEMS_JSON}...")
        with open(ITEMS_JSON, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {updated} items with local icon paths")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  ✅ Downloaded: {downloaded}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📝 Updated: {updated}")
    print(f"{'='*50}")

if __name__ == "__main__":
    try:
        process_items()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

