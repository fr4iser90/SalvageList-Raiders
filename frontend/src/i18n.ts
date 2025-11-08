// i18n translations - prepared for future German/English support
export const translations = {
  de: {
    title: 'ARC RAIDERS ITEM TRACKER',
    subtitle: 'Finde welche Items du recyceln kannst, um benötigte Materialien zu bekommen',
    materialInput: 'Material das ich brauche:',
    materialPlaceholder: 'z.B. Wires, Metal Parts, Chemicals...',
    itemsProducing: 'Items die {material} liefern:',
    noItemsFound: 'Keine Items gefunden die {material} liefern.',
    selectMaterial: 'Wähle ein Material aus, um zu sehen welche Items es liefern.',
    loading: 'Lade Items...',
    error: 'Fehler: {error}',
    recyclesTo: 'Recycelt zu:',
    sell: 'Verkauf:',
    perItem: '{quantity}x {material} pro Item',
    supportTitle: 'Projekt unterstützen',
    supportDescription: 'Wenn dir dieses Projekt gefällt, erwäge bitte die Entwicklung zu unterstützen:',
    supportHelpText: 'Deine Unterstützung hilft, die Entwicklungskosten zu decken und das Projekt aktiv zu pflegen.',
  },
  en: {
    title: 'ARC RAIDERS ITEM TRACKER',
    subtitle: 'Find which items you can recycle to get needed materials',
    materialInput: 'Material I need:',
    materialPlaceholder: 'e.g. Wires, Metal Parts, Chemicals...',
    itemsProducing: 'Items that produce {material}:',
    noItemsFound: 'No items found that produce {material}.',
    selectMaterial: 'Select a material to see which items produce it.',
    loading: 'Loading items...',
    error: 'Error: {error}',
    recyclesTo: 'Recycles to:',
    sell: 'Sell:',
    perItem: '{quantity}x {material} per item',
    supportTitle: 'Support the Project',
    supportDescription: 'If you find this project useful, please consider supporting its development:',
    supportHelpText: 'Your support helps cover development costs and keeps the project actively maintained.',
  },
};

export type Language = 'de' | 'en';

// Simple i18n helper (will be expanded later)
export function t(key: string, lang: Language = 'de', params?: Record<string, string>): string {
  const translation = translations[lang][key as keyof typeof translations.de] || key;
  if (params) {
    return translation.replace(/\{(\w+)\}/g, (_, param) => params[param] || '');
  }
  return translation;
}

