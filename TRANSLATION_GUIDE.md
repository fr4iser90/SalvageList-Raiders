# Translation Guide

## 🌍 Adding a New Language

### Step 1: Create a New Translation File

1. Copy `frontend/src/translations/TEMPLATE.ts` to `frontend/src/translations/[language-code].ts`
   - Example: `frontend/src/translations/fr.ts` for French
   - Example: `frontend/src/translations/es.ts` for Spanish
   - Example: `frontend/src/translations/it.ts` for Italian

2. Use ISO 639-1 language codes (2 letters)

### Step 2: Fill in Translations

Open the new file and fill in the translations:

```typescript
// French translations example
export const itemTranslations: Record<string, string> = {
  "Advanced ARC Powercell": "Cellule ARC Avancée",
  "Wires": "Fils",
  // ... more translations
};

export const materialTranslations: Record<string, string> = {
  "Wires": "Fils",
  "Metal Parts": "Pièces Métalliques",
  // ... more translations
};

export const categoryTranslations: Record<string, string> = {
  "Misc": "Divers",
  "Recyclable": "Recyclable",
  // ... more translations
};

export const rarityTranslations: Record<string, string> = {
  "Common": "Commun",
  "Rare": "Rare",
  // ... more translations
};
```

### Step 3: System Integration

1. **Update `frontend/src/translations.ts`:**
   ```typescript
   import * as frTranslations from './translations/fr';
   
   function getTranslations(lang: 'de' | 'en' | 'fr') {
     if (lang === 'de') return gerTranslations;
     if (lang === 'en') return enTranslations;
     if (lang === 'fr') return frTranslations;
     return enTranslations; // fallback
   }
   ```

2. **Update `frontend/src/i18n.ts`:**
   ```typescript
   export type Language = 'de' | 'en' | 'fr';
   
   export const translations = {
     de: { ... },
     en: { ... },
     fr: {
       title: 'ARC RAIDERS ITEM TRACKER',
       subtitle: 'Trouvez quels objets recycler pour obtenir les matériaux nécessaires',
       // ... more UI translations
     },
   };
   ```

3. **Update `frontend/src/App.tsx`:**
   - Add a button for the new language in the language selector

## 📝 Improving Existing Translations

### German (ger.ts)

1. Open `frontend/src/translations/ger.ts`
2. Uncomment the lines (remove `//`)
3. Replace example translations with actual names from the game

### Example:
```typescript
export const itemTranslations: Record<string, string> = {
  "Advanced ARC Powercell": "Fortgeschrittene ARC-Zelle",  // ← Actual name from game
  "Wires": "Drähte",  // ← Actual name from game
};
```

## 🎮 Where to Find Translations?

### 1. **In the Game Itself** (Best Source!)
   - Launch ARC Raiders in the desired language
   - Go to inventory/menu
   - Note down the names of items and materials
   - Screenshots help!

### 2. **Steam Community Guides**
   - Search for "ARC Raiders [Language] Items"
   - Community members sometimes create translation lists

### 3. **Game Databases**
   - Some game databases have multilingual entries
   - Check SteamDB or similar sites

## 📋 What Needs to be Translated?

- **Item Names**: The names of items themselves (e.g., "Advanced ARC Powercell")
- **Material Names**: Materials obtained from recycling (e.g., "Wires", "Metal Parts")
- **Categories**: Partially translated (Misc → Verschiedenes, etc.)
- **Rarity**: Already translated (Common → Gewöhnlich, etc.)
- **UI Texts**: In `i18n.ts` (title, buttons, etc.)

## 💡 Tips

- If you have many items:
  1. Take screenshots from the game
  2. Enter the names into an Excel/CSV file
  3. Copy them into the translation file

- Test your translations:
  ```bash
  npm run dev
  ```
  Switch to the language and verify everything displays correctly

## 🤝 Creating a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b feature/translation-french`
3. Make your changes
4. Commit: `git commit -m "Add French translations"`
5. Push: `git push origin feature/translation-french`
6. Create a Pull Request on GitHub

Thank you for your contribution! 🙏

