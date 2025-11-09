# Data Extraction Scripts

Diese Scripts werden verwendet, um Daten von der ARC Raiders Wiki zu extrahieren und zu aktualisieren.

## Scripts

### `extract_all_data.py`

Extrahiert alle Daten von der Wiki:
- **Trader-Daten** (Celeste, Tian Wen, Apollo, Shani, Lance)
- **Workshop Level-Ups** (Workbench, Gunsmith, etc.)
- **Expedition Projects**

**Ausgabe:**
- Speichert in `data/` (Source-Dateien)
- Kopiert nach `frontend/public/` (für die App)

**Verwendung:**
```bash
python3 scripts/extract_all_data.py
```

### `download_icons.py`

Lädt Item-Icons von der Wiki herunter und aktualisiert `data/items.json` mit lokalen Pfaden.

**Verwendung:**
```bash
python3 scripts/download_icons.py
```

## Projektstruktur

```
SalvageList-Raiders/
├── scripts/              # Data extraction scripts
│   ├── extract_all_data.py
│   └── download_icons.py
├── data/                 # Source-Dateien (vom Script erstellt)
│   ├── items.json
│   ├── materials-info.json
│   ├── workshop_level_ups.json
│   └── expedition_projects.json
└── frontend/
    └── public/           # Dateien für die App (vom Script kopiert)
        ├── items.json
        ├── materials-info.json
        ├── workshop_level_ups.json
        └── expedition_projects.json
```

## Wann Scripts ausführen?

Die Scripts sind **nicht** für den normalen Betrieb der App nötig. Sie werden nur benötigt, wenn:

- Neue Items/Materialien in der Wiki hinzugefügt wurden
- Trader-Daten aktualisiert werden müssen
- Neue Icons heruntergeladen werden sollen
- Workshop/Project-Daten geändert wurden

## Hinweise

- Die Scripts arbeiten mit relativen Pfaden vom Projekt-Root
- Sie können von überall ausgeführt werden (Pfade werden automatisch berechnet)
- Die Scripts erstellen/kopieren automatisch die benötigten Verzeichnisse

