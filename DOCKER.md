# Docker Setup für Arc Raiders Item Tracker

## Build & Start

```bash
# Build und Start
docker-compose up -d --build

# Logs ansehen
docker-compose logs -f

# Stoppen
docker-compose down
```

## Port

Die App läuft auf **Port 3000**: http://localhost:3000

## Produktions-Build

Das Dockerfile erstellt einen optimierten Produktions-Build:
- Multi-stage build (kleineres Image)
- Nginx als Webserver
- Gzip-Kompression
- Security Headers
- Caching für statische Assets

## Image bauen und pushen

```bash
# Build
docker build -t fr4iser/salvageARC:latest .

# Push (falls gewünscht)
docker push fr4iser/salvageARC:latest
```

## Health Check

Der Container hat einen Health Check integriert. Status prüfen:
```bash
docker ps
# HEALTHY Status sollte angezeigt werden
```

