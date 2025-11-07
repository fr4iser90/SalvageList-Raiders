# Arc Raiders Item Tracker - UI Konzept & Tech-Stack

## 🎯 Projekt-Ziel
Eine Web-App zum Finden, welche Items man recyceln kann, um benötigte Materialien zu bekommen.

**Workflow:**
1. User wählt ein Material aus, das er BRAUCHT (z.B. "Wires")
2. App zeigt: Welche Items kann ich recyceln, um dieses Material zu bekommen?
3. App zeigt: Wie viele von jedem Item brauche ich?

**Beispiel:**
- Brauche: "Wires"
- App zeigt:
  - "Advanced Electrical Components" → recycelt zu "1x Wires" (brauche 1x Item)
  - "Broken Handheld Radio" → recycelt zu "2x Wires" (brauche 1x Item für 2x Wires)
  - "Cooling Fan" → recycelt zu "4x Wires" (brauche 1x Item für 4x Wires)

## 🛠️ Tech-Stack

### Frontend: **React + Vite + TypeScript**
- ✅ React: Bewährt, große Community
- ✅ Vite: Schnellster Dev-Server
- ✅ TypeScript: Type-Safety

### Styling: **Tailwind CSS v4**
- ✅ v4 ist die aktuelle Version (Januar 2025)
- ✅ Modernste Features
- ✅ CSS-basierte Konfiguration

### State Management: **React useState/useEffect**
- ✅ Für diese App ausreichend
- ✅ Keine zusätzlichen Dependencies

### Daten-Persistenz: **LocalStorage**
- ✅ Speichert welche Materialien der User braucht

## 🎨 UI Design

### Layout-Struktur

```
┌─────────────────────────────────────────┐
│  Header                                  │
│  🎮 ARC RAIDERS ITEM TRACKER             │
├─────────────────────────────────────────┤
│  Material auswählen:                     │
│  [Dropdown: Wires ▼]                    │
│  Brauche: [5]                            │
├─────────────────────────────────────────┤
│                                         │
│  Items die dieses Material liefern:     │
│  ┌─────────────────────┐               │
│  │ Advanced Electrical  │               │
│  │ Components           │               │
│  │ → 1x Wires           │               │
│  │ Brauche: 5x Items    │               │
│  └─────────────────────┘               │
│                                         │
└─────────────────────────────────────────┘
```

### Features
1. **Material-Auswahl**: Dropdown mit allen Materialien
2. **Menge eingeben**: Wie viele brauche ich?
3. **Item-Liste**: Zeigt alle Items die dieses Material liefern
4. **Berechnung**: Wie viele Items brauche ich für X Materialien?

## 📋 Features (MVP)

- [x] Alle Materialien aus Items extrahieren
- [x] Material-Auswahl Dropdown
- [x] Menge eingeben
- [x] Items filtern die dieses Material liefern
- [x] Berechnung: Wie viele Items brauche ich?
- [x] Sortierung: Beste Items zuerst (meiste Materialien pro Item)
