// Item name translations: English -> German
// This file maps English item names from the wiki to German names from the game
// Fill this out by checking the game itself or community resources

export const itemTranslations: Record<string, string> = {
  // Example entries - replace with actual German names from the game
  // "Advanced ARC Powercell": "Fortgeschrittene ARC-Zelle",
  // "Wires": "Drähte",
  // "Metal Parts": "Metallteile",
  // "Chemicals": "Chemikalien",
  // "Electrical Components": "Elektrische Komponenten",
  // "Mechanical Components": "Mechanische Komponenten",
  // "Steel Spring": "Stahlfeder",
  // "ARC Powercell": "ARC-Zelle",
  // "Plastic Parts": "Kunststoffteile",
  // "Processor": "Prozessor",
  // "Rubber Parts": "Gummiteile",
  // "Fabric": "Stoff",
  // "ARC Alloy": "ARC-Legierung",
  // "ARC Circuitry": "ARC-Schaltkreis",
  // "ARC Coolant": "ARC-Kühlmittel",
  // "ARC Flex Rubber": "ARC-Flexgummi",
  // "ARC Motion Core": "ARC-Bewegungskern",
  // "ARC Performance Steel": "ARC-Leistungsstahl",
  // "ARC Synthetic Resin": "ARC-Synthetisches Harz",
  // "ARC Thermo Lining": "ARC-Thermoauskleidung",
  // "Agave": "Agave",
  // "Agave Juice": "Agavensaft",
  // "Air Freshener": "Lufterfrischer",
  // "Alarm Clock": "Wecker",
  // "Antiseptic": "Antiseptikum",
  // "Apricot": "Aprikose",
  // "Assorted Seeds": "Verschiedene Samen",
  // "Canister": "Kanister",
  // "Durable Cloth": "Langlebiger Stoff",
  // "Oil": "Öl",
  // "Sensors": "Sensoren",
  // "Simple Gun Parts": "Einfache Waffenteile",
  // "Torn Book": "Zerrissenes Buch",
  // "Torn Blanket": "Zerrissene Decke",
  // "Tattered ARC Lining": "Zerfetzte ARC-Auskleidung",
  // "Tattered Clothes": "Zerfetzte Kleidung",
  // "Tick Pod": "Zeckenkapsel",
  // "Toaster": "Toaster",
  // "Turbo Pump": "Turbolader",
  // "Unusable Weapon": "Unbrauchbare Waffe",
  // "Vase": "Vase",
  // "Very Comfortable Pillow": "Sehr bequemes Kissen",
  // "Volcanic Rock": "Vulkanisches Gestein",
  // "Voltage Converter": "Spannungswandler",
  // "Wasp Driver": "Wespen-Treiber",
  // "Water Filter": "Wasserfilter",
  // "Water Pump": "Wasserpumpe",
  // "Statuette": "Statuette",
  // "Syringe": "Spritze",
  // "Surveyor Vault": "Vermessungs-Tresor",
  // "Synthesized Fuel": "Synthetischer Kraftstoff",
  // "Thermostat": "Thermostat",
};

// Material name translations: English -> German
export const materialTranslations: Record<string, string> = {
  // Example entries - replace with actual German names from the game
  // "Wires": "Drähte",
  // "Metal Parts": "Metallteile",
  // "Chemicals": "Chemikalien",
  // "Electrical Components": "Elektrische Komponenten",
  // "Mechanical Components": "Mechanische Komponenten",
  // "Steel Spring": "Stahlfeder",
  // "ARC Powercell": "ARC-Zelle",
  // "Plastic Parts": "Kunststoffteile",
  // "Processor": "Prozessor",
  // "Rubber Parts": "Gummiteile",
  // "Fabric": "Stoff",
  // "ARC Alloy": "ARC-Legierung",
  // "Oil": "Öl",
  // "Sensors": "Sensoren",
  // "Simple Gun Parts": "Einfache Waffenteile",
  // "Assorted Seeds": "Verschiedene Samen",
  // "Canister": "Kanister",
  // "Durable Cloth": "Langlebiger Stoff",
};

// Category translations: English -> German
export const categoryTranslations: Record<string, string> = {
  "Misc": "Verschiedenes",
  "Refined Material": "Raffiniertes Material",
  "Nature": "Natur",
  "Quick Use": "Schnellverwendung",
  "Trinket": "Kuriosität",
  "Recyclable": "Recycelbar",
  "Topside Material": "Oberflächenmaterial",
};

// Rarity translations: English -> German
export const rarityTranslations: Record<string, string> = {
  "Common": "Gewöhnlich",
  "Uncommon": "Ungewöhnlich",
  "Rare": "Selten",
  "Epic": "Episch",
  "Legendary": "Legendär",
  "Uncomon": "Ungewöhnlich", // Typo in original data
};

// Helper function to translate item names
export function translateItemName(name: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return name;
  return itemTranslations[name] || name;
}

// Helper function to translate material names
export function translateMaterialName(name: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return name;
  return materialTranslations[name] || name;
}

// Helper function to translate category names
export function translateCategoryName(category: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return category;
  return categoryTranslations[category] || category;
}

// Helper function to translate rarity names
export function translateRarityName(rarity: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return rarity;
  return rarityTranslations[rarity] || rarity;
}

