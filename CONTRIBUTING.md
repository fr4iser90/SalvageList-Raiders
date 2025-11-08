# Contributing

Thank you for wanting to help! 🎉

## Contributing Translations

### Adding a New Language

1. **Create a new translation file:**
   - Copy `frontend/src/translations/TEMPLATE.ts` to `frontend/src/translations/[language-code].ts`
   - Use ISO 639-1 language codes (e.g., `fr.ts` for French, `es.ts` for Spanish, `it.ts` for Italian)
   - Or copy `frontend/src/translations/en.ts` as a starting point

2. **Fill in the translations:**
   ```typescript
   export const itemTranslations: Record<string, string> = {
     "Advanced ARC Powercell": "Translation here",
     "Wires": "Translation here",
     // ... more translations
   };
   ```

3. **Update `frontend/src/translations.ts`:**
   - Import the new language file
   - Add it to `getTranslations()` function
   - Update the function signatures to include the new language

4. **Update `frontend/src/i18n.ts`:**
   - Add the new language to the `translations` object
   - Add it to the `Language` type
   - Add UI text translations (title, subtitle, buttons, etc.)

5. **Update `frontend/src/App.tsx`:**
   - Add a button for the new language in the language selector

### Improving Existing Translations

1. **Open the corresponding file:**
   - German: `frontend/src/translations/ger.ts`
   - English: `frontend/src/translations/en.ts`

2. **Add or correct translations:**
   ```typescript
   export const itemTranslations: Record<string, string> = {
     "Item Name": "Translation here",
   };
   ```

3. **Test your translations:**
   - Start the app: `npm run dev`
   - Switch to the language and verify the translations

## Creating a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b feature/translation-french`
3. Make your changes
4. Commit: `git commit -m "Add French translations"`
5. Push: `git push origin feature/translation-french`
6. Create a Pull Request on GitHub

## Where to Find Translations?

### In the Game Itself (Best Source!)
- Launch ARC Raiders in the desired language
- Go to inventory/menu
- Note down the names of items and materials
- Screenshots help!

### Community Resources
- Steam Community Guides
- Game databases
- Discord/Reddit communities

## Translation File Structure

Each translation file contains:

- `itemTranslations`: Item names (e.g., "Advanced ARC Powercell")
- `materialTranslations`: Material names (e.g., "Wires", "Metal Parts")
- `categoryTranslations`: Categories (e.g., "Misc", "Recyclable")
- `rarityTranslations`: Rarities (e.g., "Common", "Rare")

## Questions?

Open an issue on GitHub or contact the maintainer.

Thank you for your contribution! 🙏

