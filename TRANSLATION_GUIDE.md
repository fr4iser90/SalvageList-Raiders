# Übersetzungsanleitung für Arc Raiders Items

## Wo finde ich die deutschen Übersetzungen?

### 1. **Im Spiel selbst** (Beste Quelle!)
   - Starte Arc Raiders auf Deutsch
   - Gehe ins Inventar/Menü
   - Notiere die deutschen Namen der Items und Materialien
   - Screenshots machen hilft!

### 2. **Steam Community Guides**
   - Suche nach "Arc Raiders German Items" oder ähnlich
   - Community-Mitglieder haben manchmal Übersetzungslisten erstellt

### 3. **Spiel-Datenbanken**
   - Manche Spiele-Datenbanken haben mehrsprachige Einträge
   - Prüfe SteamDB oder ähnliche Seiten

## Wie trage ich die Übersetzungen ein?

1. Öffne `frontend/src/translations.ts`
2. Entkommentiere die Zeilen (entferne `//` am Anfang)
3. Ersetze die Beispiel-Übersetzungen mit den echten deutschen Namen aus dem Spiel

### Beispiel:
```typescript
export const itemTranslations: Record<string, string> = {
  "Advanced ARC Powercell": "Fortgeschrittene ARC-Zelle",  // ← Echter Name aus dem Spiel
  "Wires": "Drähte",  // ← Echter Name aus dem Spiel
  // ... usw.
};
```

## Wichtige Hinweise:

- **Item-Namen**: Die Namen der Items selbst (z.B. "Advanced ARC Powercell")
- **Material-Namen**: Die Materialien die beim Recyceln rauskommen (z.B. "Wires", "Metal Parts")
- **Kategorien**: Sind bereits übersetzt (Misc → Verschiedenes, etc.)
- **Rarity**: Ist bereits übersetzt (Common → Gewöhnlich, etc.)

## Tipp:

Falls du viele Items hast, kannst du:
1. Screenshots aus dem Spiel machen
2. Die Namen in eine Excel/CSV-Datei eintragen
3. Dann in die `translations.ts` kopieren

Die Struktur ist vorbereitet - du musst nur die Übersetzungen eintragen! 🎮

