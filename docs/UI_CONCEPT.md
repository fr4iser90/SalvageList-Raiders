# UI/UX Konzept: Material-Darstellung (Cheat Sheet)

## Übersicht

Einheitliches, klares Design für Material-Informationen mit eindeutigen Icons und vollständigen Informationen.
**Ziel**: Schnell finden, wo man Materialien herbekommt (Recycling, Trading, Maps).

## Sortierung: Nach Materialien (nicht nach Maps)

**Warum nach Materialien?**
- ✅ User-Denkweise: "Ich brauche Metal Parts - wo bekomme ich die her?"
- ✅ Alle Infos an einem Ort: Recycling, Trading, Map-Locations
- ✅ Schneller Zugriff: Material suchen → alles sehen
- ✅ Maps sind sekundär: Man sucht Material, nicht Map

**Nach Maps wäre schlechter:**
- ❌ User muss wissen, welche Map welches Material hat
- ❌ Material-Info ist über mehrere Maps verteilt
- ❌ Unpraktisch für Cheat Sheet

---

## 1. Material-Übersicht (Tab: "Materials")

### Layout
- **Grid-Layout**: Material-Cards in einem responsiven Grid (3-4 Spalten auf Desktop, 2 auf Tablet, 1 auf Mobile)
- **Jede Material-Card** zeigt:
  - **Icon** (groß, zentral, 64x64px) - eindeutig erkennbar
  - **Material-Name** (fett, groß)
  - **Kurze Info-Badges**:
    - 🛒 "Available at Trader" (wenn verfügbar)
    - 🔨 "Used in Workshop" (wenn verwendet)
    - 📦 "Used in Projects" (wenn verwendet)
    - ♻️ "Recyclable" (wenn Items es produzieren)
  - **Hover-Effekt**: Card hebt sich leicht an, Border wird heller

### Design der Material-Card
```
┌─────────────────────────┐
│                         │
│      [ICON 64x64]      │
│                         │
│    Material Name        │
│                         │
│  🛒 Trader  🔨 Workshop │
└─────────────────────────┘
```

**Styling:**
- `bg-gray-800` Hintergrund
- `border border-gray-700` Border
- `rounded-lg` Ecken
- `p-4` Padding
- `hover:border-gray-600 hover:shadow-lg` Hover-Effekt
- Icon: `w-16 h-16` (64x64px), zentriert

---

## 2. Material-Detailansicht (beim Klicken auf Material-Card)

### Modal/Drawer oder erweiterte Ansicht

**Option A: Modal (empfohlen)**
- Overlay mit Material-Details
- Schließbar mit X-Button oder Klick außerhalb
- Scrollbar wenn Inhalt zu lang

**Option B: Erweiterte Card**
- Card expandiert in der Übersicht
- Andere Cards werden kleiner/ausgeblendet

### Detailansicht-Inhalt

#### Header
- **Großes Icon** (128x128px) - zentral oben
- **Material-Name** (groß, fett)
- **Kurzbeschreibung** (optional, falls vorhanden)
- **🗺️ Map-Icon Button** (NUR wenn mapLocations vorhanden) - rechts oben neben X-Button
  - Klick öffnet separates Map-Locations-Modal
  - Nur sichtbar wenn Material Map-Locations hat

#### Tabs innerhalb der Detailansicht

**Tab 1: ♻️ Recycling**
- **Überschrift**: "Items that produce this material"
- **Liste von ItemResultCards** (wie aktuell)
- Jede Card zeigt:
  - Item-Icon
  - Item-Name
  - Rarity-Badge
  - **"Produces: 2x Material Name"** (hervorgehoben)
  - Sell Price
  - Recycle-Info

**Tab 2: 🛒 Trading**
- **Überschrift**: "Available at Traders"
- **Trader-Cards**:
  ```
  ┌─────────────────────────┐
  │ 🛒 Trader Name          │
  │                         │
  │ Price: Assorted Seeds x1│
  │ Frequency: Daily        │
  │ Reset: 01:00 UTC+1     │
  └─────────────────────────┘
  ```
- Falls mehrere Trader: Alle anzeigen
- Falls nicht verfügbar: "Not available at any trader"

**Tab 3: 🔨 Workshop**
- **Überschrift**: "Used in Workshop Upgrades"
- **Station-Cards**:
  ```
  ┌─────────────────────────┐
  │ 🔨 Station Name         │
  │                         │
  │ Level 2:                │
  │   • 20x Material Name   │
  │   • 30x Other Material  │
  │                         │
  │ Level 3:                │
  │   • 5x Material Name    │
  └─────────────────────────┘
  ```
- Jedes Material mit Icon
- Falls nicht verwendet: "Not used in workshop"

**Tab 4: 📦 Projects**
- **Überschrift**: "Required for Expedition Projects"
- **Project-Cards**:
  ```
  ┌─────────────────────────┐
  │ 📦 Project Name         │
  │                         │
  │ Description: ...        │
  │                         │
  │ Required:               │
  │   • 150x Material Name  │
  │   • 200x Other Material │
  └─────────────────────────┘
  ```
- Jedes Material mit Icon
- Falls nicht verwendet: "Not required for any project"

**Tab 5: 🔧 Crafting** (falls vorhanden)
- **Überschrift**: "Crafting Recipes"
- Zeigt, was man mit diesem Material craften kann
- Recipe-Cards mit:
  - Crafted Item (mit Icon)
  - Required Materials (alle mit Icons)
  - Station & Level

---

## 3. Icon-System

### Icon-Quelle
- **Primär**: Aus `items.json` - suche Item, das dieses Material beim Recycling produziert
- **Fallback 1**: Suche Item, das beim Recycling dieses Material produziert (exakter Match)
- **Fallback 2**: Suche Item mit ähnlichem Namen
- **Fallback 3**: Placeholder-Icon (Material-Symbol)

### Icon-Größen
- **Material-Card**: `w-16 h-16` (64x64px)
- **Detailansicht Header**: `w-32 h-32` (128x128px)
- **In Listen (Workshop/Projects)**: `w-8 h-8` (32x32px)
- **In ItemResultCards**: `w-16 h-16` (64x64px) - bereits so

### Icon-Suche-Logik
```typescript
function getMaterialIcon(materialName: string, items: Item[]): string | null {
  // 1. Exakter Match: Item produziert genau dieses Material
  const exactMatch = items.find(item => {
    const materials = parseRecycleString(item.recycles);
    return materials.some(m => m.material === materialName);
  });
  if (exactMatch?.image) return exactMatch.image;
  
  // 2. Item-Name Match: Item-Name ähnelt Material-Name
  const nameMatch = items.find(item => 
    item.name.toLowerCase().includes(materialName.toLowerCase()) ||
    materialName.toLowerCase().includes(item.name.toLowerCase())
  );
  if (nameMatch?.image) return nameMatch.image;
  
  // 3. Placeholder
  return null; // oder Placeholder-Icon
}
```

---

## 4. Navigation & Tabs

### Haupt-Tabs (oben)
1. **Materials** - Material-Übersicht
2. **Workshop** - Workshop-Stationen & Level-Ups
3. **Projects** - Expedition Projects

### Material-Detail-Tabs (innerhalb der Detailansicht)
**Nur Tabs anzeigen, die Daten haben:**
1. ♻️ Recycling (wenn Items es produzieren) - **STANDARD-TAB**
2. 🛒 Trading (wenn bei Trader verfügbar)
3. 🔨 Workshop (wenn in Workshop verwendet)
4. 📦 Projects (wenn in Projects benötigt)
5. 🔧 Crafting (falls vorhanden)

**Tab-Reihenfolge nach Wichtigkeit:**
- **Recycling: IMMER zuerst** (Standard-Tab) - Meiste Materialien kommen daher
- Trading: Alternative Quelle
- Workshop/Projects: Verwendung (nicht Beschaffung)

**WICHTIG**: 
- Tabs werden dynamisch angezeigt - nur wenn Daten vorhanden sind!
- **Map Locations ist KEIN Tab** - es ist ein separates Feature mit Button/Icon im Header

---

## 5. Interaktivität

### Material-Card Klick
- Öffnet Material-Detailansicht (Modal)
- **Standard-Tab: IMMER "♻️ Recycling"** (wenn verfügbar)
- Falls Recycling nicht verfügbar: Erster verfügbarer Tab
- **Map Locations**: Separates Feature - nicht als Tab, sondern als Button/Icon im Header

### Material-Icon in Listen
- Klick auf Icon öffnet auch Material-Detailansicht
- Hover: Tooltip mit Material-Name

### Trader-Info
- Klick auf Trader-Name: Zeigt alle Materialien dieses Traders
- Reset-Zeit: Hervorgehoben, mit Countdown (optional)

### Map Locations (Separates Feature - KEIN Tab)
- **🗺️ Map-Icon Button** im Header der Material-Detailansicht (rechts oben)
- **NUR sichtbar** wenn Material `mapLocations` hat (ganz wenige Materialien)
- **Klick auf Map-Icon**: Öffnet separates Map-Locations-Modal
- **Map-Locations-Modal zeigt**:
  - Material-Name & Icon
  - Screenshot der Map (PRO MAP EIN SCREENSHOT)
  - Marker/Pfeil zeigt exakte Spawn-Stelle für dieses Material
  - Location: Area Name
  - Spawn Rate: Common/Uncommon/Rare
  - Notes: "Near building", "In containers", etc.
  - **Klick auf Screenshot**: Lightbox öffnet (Fullscreen für Details)
- **WICHTIG**: Map Locations ist optional und selten - nur bei ganz wenigen Materialien!

---

## 6. Design-System

### Farben
- **Hintergrund**: `bg-gray-900` (Haupt), `bg-gray-800` (Cards)
- **Borders**: `border-gray-700` (normal), `border-gray-600` (hover)
- **Text**: `text-gray-100` (Haupt), `text-gray-400` (Sekundär)
- **Akzente**: 
  - Recycling: `bg-blue-900/30 border-blue-700`
  - Trading: `bg-green-900/30 border-green-700`
  - Workshop: `bg-purple-900/30 border-purple-700`
  - Projects: `bg-yellow-900/30 border-yellow-700`

### Typografie
- **Material-Name**: `text-lg font-bold`
- **Überschriften**: `text-xl font-bold`
- **Body**: `text-sm`
- **Labels**: `text-xs text-gray-400`

### Spacing
- **Card Padding**: `p-4`
- **Grid Gap**: `gap-4`
- **Section Margin**: `mb-6`

---

## 7. Responsive Design

### Desktop (>1024px)
- 4 Spalten für Material-Grid
- Modal: 800px breit, zentriert

### Tablet (768px-1024px)
- 3 Spalten für Material-Grid
- Modal: 90% Breite

### Mobile (<768px)
- 2 Spalten für Material-Grid
- Modal: Fullscreen
- Tabs: Scrollbar horizontal

---

## 8. Datenstruktur

### MaterialInfo (erweitert)
```typescript
interface MaterialInfo {
  material: string;
  icon?: string; // Icon-URL
  
  // Map Locations (NEU - OPTIONAL, nur bei bestimmten Materialien)
  mapLocations?: Array<{
    mapName: string;
    areaName?: string; // Optional, falls mehrere Areas
    screenshot: string; // Screenshot-URL (PRO MAP EIN SCREENSHOT, z.B. dam_battlegrounds_full.png, buried_city_full.png, spaceport_full.png, the_blue_gate_full.png)
    marker: {
      x: number; // X-Position des Markers auf Screenshot (0-100% oder Pixel)
      y: number; // Y-Position des Markers auf Screenshot
      color?: string; // Optional: Marker-Farbe für dieses Material
    };
    spawnRate: 'Common' | 'Uncommon' | 'Rare';
    notes?: string; // "Near building", "In containers", etc.
  }>;
  // WICHTIG: mapLocations ist optional - nur bei Materialien mit Screenshots vorhanden
  // PRO MAP EIN SCREENSHOT, mehrere Marker für verschiedene Materialien auf derselben Map
  
  // Trading
  trader?: {
    available: boolean;
    trader_name: string;
    price: string;
    frequency: string;
  };
  
  // Recycling (Items die es produzieren)
  recycledFrom?: Array<{
    item: Item;
    quantity: number;
  }>;
  
  // Workshop (wo wird es verwendet)
  usedInWorkshop?: Array<{
    station: string;
    level: string;
    quantity: number;
  }>;
  
  // Projects (wo wird es benötigt)
  usedInProjects?: Array<{
    project: string;
    quantity: number;
  }>;
  
  // Crafting (was kann man damit craften)
  craftingRecipes?: Array<{
    item: string;
    station: string;
    level: string;
    requiredMaterials: MaterialQuantity[];
  }>;
}
```

### Screenshot-Struktur: PRO MAP EIN SCREENSHOT

**Ansatz: Ein Screenshot pro Map mit Markierungen**
```
frontend/public/screenshots/
  └── maps/
      ├── dam_battlegrounds_full.png
      ├── buried_city_full.png
      ├── spaceport_full.png
      ├── the_blue_gate_full.png
      └── stella_montis_full.png (später)
```

**Maps in ARC Raiders:**
1. **Dam Battlegrounds** - Sumpfiges, bewaldetes Gebiet
2. **Buried City** - Verschüttete Metropole
3. **Spaceport** - Überreste von Acerra
4. **The Blue Gate** - Hoch in den Bergen
5. **Stella Montis** - Kommt später (November 2025)

**WICHTIG:**
- ✅ **PRO MAP EIN SCREENSHOT** (nicht ein Screenshot für alle!)
- ✅ Jede Map hat ihren eigenen Screenshot
- ✅ Marker für verschiedene Materialien auf dem Screenshot ihrer jeweiligen Map

**Marker-System:**
- Jeder Screenshot zeigt eine Map
- **Marker/Pfeile** zeigen exakte Spawn-Stellen für verschiedene Materialien auf dieser Map
- **Farbcodierung** pro Material:
  - Lightbulb = 🔵 Blauer Marker
  - Metal Parts = 🟢 Grüner Marker
  - Wires = 🟡 Gelber Marker
  - Battery = 🟣 Lila Marker
  - etc.
- **Text-Labels** neben Markern: Material-Name

**Beim Öffnen des Map-Locations-Modals:**
- Screenshot der entsprechenden Map wird angezeigt
- Marker für dieses Material wird hervorgehoben
- **WICHTIG**: Map Locations ist optional und selten - nur bei ganz wenigen Materialien!

### Screenshot-Struktur (Option 2: Viele Screenshots - nicht empfohlen)
```
frontend/public/screenshots/
  └── materials/
      ├── metal_parts/
      │   ├── dam_battlegrounds_area1.png
      │   └── buried_city_area1.png
      └── wires/
          └── spaceport_area1.png
```
**Nachteil**: Viele Dateien, redundante Screenshots

---

## 9. Implementierungs-Reihenfolge

1. ✅ **Material-Übersicht mit Icons** (Grid-Layout)
2. ✅ **Material-Detailansicht (Modal)**
3. ✅ **Tab: Recycling** (bestehende ItemResultCards)
4. ✅ **Tab: Trading** (Trader-Info)
5. ✅ **Tab: Workshop** (Station-Info)
6. ✅ **Tab: Projects** (Project-Info)
7. ✅ **Map Locations Feature** (OPTIONAL - nur wenn Screenshots vorhanden) - **Separates Modal, nicht als Tab**
8. ✅ **Icon-Suche-Logik** (für alle Materialien)
9. ✅ **Screenshot-Integration** (Bildanzeige, Lightbox für Zoom) - **Nur wenn mapLocations vorhanden**
10. ✅ **Dynamische Tab-Anzeige** (nur Tabs mit Daten anzeigen)
11. ✅ **Responsive Design**

## 10. Map Locations Feature (Separates Modal)

### Map-Icon Button im Header
- **Position**: Rechts oben neben X-Button
- **NUR sichtbar** wenn Material `mapLocations` hat
- **Icon**: 🗺️ (Map-Icon)
- **Hover**: Tooltip "Show map locations"
- **Klick**: Öffnet Map-Locations-Modal

### Map-Locations-Modal
- **Separates Modal** (nicht als Tab!)
- **Header**: Material-Name & Icon
- **Inhalt**: 
  - Map-Name (z.B. "Dam Battlegrounds")
  - Screenshot der Map (800x600px oder größer)
  - Marker/Pfeil zeigt exakte Spawn-Stelle für dieses Material
  - Location: Area Name
  - Spawn Rate: Common/Uncommon/Rare
  - Notes: "Near building", "In containers", etc.
- **Klick auf Screenshot**: Lightbox öffnet (Fullscreen für Details)
- **Schließen**: ESC oder X-Button

### Screenshot-Anzeige
- **In Map-Locations-Modal**: Screenshot groß (800x600px oder größer)
- **Klick auf Screenshot**: Lightbox öffnet (Fullscreen/Modal)
- **Lightbox Features**:
  - Vollbild-Screenshot
  - Zoom-Funktion (optional)
  - Map-Name & Area-Name als Caption
  - Navigation zwischen mehreren Screenshots (falls mehrere Locations)
  - Schließen mit ESC oder X-Button

### Screenshot-Qualität
- **Format**: PNG oder WebP (für bessere Kompression)
- **Auflösung**: Mindestens 1920x1080 (für Details)
- **Thumbnail**: Automatisch generiert oder separate kleine Version
- **Lazy Loading**: Screenshots erst laden wenn Map-Locations-Modal geöffnet wird

### Screenshot-Markierungen

**Ansatz 1: Marker direkt auf Screenshot (einfach) - EMPFOHLEN**
- **PRO MAP EIN SCREENSHOT** (Format: `[map_name]_full.png`)
- **Verschiedene Materialien** bekommen Marker auf dem Screenshot ihrer jeweiligen Map
- Screenshot wird mit Markern/Pfeilen erstellt (z.B. in GIMP/Photoshop)
- **Farbcodierung pro Material**:
  - Verschiedene Farben für verschiedene Materialien
  - Jedes Material hat seine eigene Farbe
- **Text-Labels** neben Markern: Material-Name
- **Spawn Rate** durch Marker-Größe oder Symbol:
  - Common = Großer Marker
  - Uncommon = Mittlerer Marker
  - Rare = Kleiner Marker
- **Beim Öffnen eines Materials**: Screenshot der entsprechenden Map wird angezeigt, Marker für dieses Material wird hervorgehoben

**Ansatz 2: Dynamische Marker (Overlay) - fortgeschritten**
- Base Screenshot: Map ohne Marker (sauberer Screenshot pro Map)
- Marker werden per CSS/JavaScript dynamisch platziert
- **Nur Marker für ausgewähltes Material** werden angezeigt
- **Vorteil**: 
  - Screenshot bleibt sauber (keine Marker sichtbar)
  - Verschiedene Materialien können denselben Screenshot nutzen
  - Marker werden nur bei Bedarf angezeigt
- Marker-Position in Datenstruktur: `{ x: 45%, y: 32% }` (Prozent oder Pixel)

**Empfehlung**: Ansatz 1 (Marker direkt auf Screenshot) - einfacher zu implementieren und zu pflegen

---

## 10. Beispiel-Screens

### Material-Übersicht
```
┌─────────────────────────────────────────┐
│  Materials  │  Workshop  │  Projects   │
├─────────────────────────────────────────┤
│ ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐   │
│ │ 🔩 │  │ ⚙️  │  │ 🔋 │  │ 🧵 │   │
│ │Metal│  │Gear │  │Batt │  │Fabr │   │
│ │Parts│  │Part │  │ery  │  │ic   │   │
│ │🛒🔨│  │🛒  │  │🛒  │  │🛒🔨│   │
│ └─────┘  └─────┘  └─────┘  └─────┘   │
└─────────────────────────────────────────┘
```

### Material-Detail (Modal) - MIT Map Locations
```
┌─────────────────────────────────────────┐
│  [ICON 128x128]        [🗺️] [X]        │
│  Metal Parts                            │
├─────────────────────────────────────────┤
│♻️ Recycling│🛒 Trading│🔨 Workshop│📦 Projects│
├─────────────────────────────────────────┤
│ Items that produce Metal Parts:          │
│                                          │
│ ┌─────────────────────────────────────┐ │
│ │ [Item Icon]  Item Name               │ │
│ │              Produces: 2x Metal Parts│ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```
**Klick auf 🗺️ öffnet Map-Locations-Modal:**
```
┌─────────────────────────────────────────┐
│  Metal Parts                    [X]     │
├─────────────────────────────────────────┤
│                                          │
│  🗺️ Dam Battlegrounds                    │
│  [SCREENSHOT 800x600 mit Marker]        │
│                                          │
│  Location: Near Alcantara Power Plant   │
│  Spawn Rate: Common                     │
│  Notes: Near building entrance          │
│                                          │
└─────────────────────────────────────────┘
```

### Material-Detail (Modal) - OHNE Map Locations
```
┌─────────────────────────────────────────┐
│  [ICON 128x128]              [X]        │
│  Wires                                   │
├─────────────────────────────────────────┤
│♻️ Recycling│🛒 Trading│🔨 Workshop│📦 Projects│
├─────────────────────────────────────────┤
│ Items that produce Wires:                │
│                                          │
│ ┌─────────────────────────────────────┐ │
│ │ [Item Icon]  Item Name               │ │
│ │              Produces: 2x Wires      │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```
**WICHTIG**: 
- Map-Icon Button (🗺️) erscheint NUR im Header, wenn mapLocations vorhanden sind
- Map Locations ist KEIN Tab - es ist ein separates Modal
- Standard-Tab ist IMMER Recycling

---

## Zusammenfassung

- **Eindeutige Icons** für jedes Material (64x64px in Cards, 128x128px in Details)
- **Einheitliches Design** mit konsistenten Cards
- **Vollständige Informationen** in Tabs (Recycling, Trading, Workshop, Projects)
- **🗺️ Map Locations**: Separates Feature mit Button/Icon im Header - NUR bei ganz wenigen Materialien
- **Standard-Tab**: IMMER Recycling (wenn verfügbar)
- **Dynamische Tabs**: Nur Tabs anzeigen, die Daten haben
- **Interaktivität** durch Klick auf Material-Card → Detailansicht
- **Responsive** für alle Geräte

**WICHTIG**: 
- Map Locations ist OPTIONAL und SELTEN - nur bei ganz wenigen Materialien!
- Map Locations ist KEIN Tab - es ist ein separates Modal mit Button/Icon im Header
- Standard-Tab ist IMMER Recycling (Hauptquelle für Materialien)

