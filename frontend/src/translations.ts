// Translation system - imports translations from language-specific files
import * as gerTranslations from './translations/ger';
import * as enTranslations from './translations/en';

// Re-export translations based on language
function getTranslations(lang: 'de' | 'en') {
  return lang === 'de' ? gerTranslations : enTranslations;
}

// Re-export for backward compatibility
export const itemTranslations = gerTranslations.itemTranslations;
export const materialTranslations = gerTranslations.materialTranslations;
export const categoryTranslations = gerTranslations.categoryTranslations;
export const rarityTranslations = gerTranslations.rarityTranslations;

// Helper function to translate item names
export function translateItemName(name: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return name;
  const translations = getTranslations(lang);
  return translations.itemTranslations[name] || name;
}

// Helper function to translate material names
export function translateMaterialName(name: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return name;
  const translations = getTranslations(lang);
  return translations.materialTranslations[name] || name;
}

// Helper function to translate category names
export function translateCategoryName(category: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return category;
  const translations = getTranslations(lang);
  return translations.categoryTranslations[category] || category;
}

// Helper function to translate rarity names
export function translateRarityName(rarity: string, lang: 'de' | 'en'): string {
  if (lang === 'en') return rarity;
  const translations = getTranslations(lang);
  return translations.rarityTranslations[rarity] || rarity;
}

