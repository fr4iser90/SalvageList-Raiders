# ARC Raiders Item Tracker

A web application to help ARC Raiders players find which items they can recycle to obtain specific materials. Search for any material and see all items that produce it when recycled.

## Features

- 🔍 **Material Search**: Search for any material and find all items that produce it
- 🌍 **Multi-language Support**: Currently supports English and German (more languages welcome!)
- 📊 **Detailed Item Information**: See rarity, category, sell price, and recycling output for each item
- 🎨 **Modern UI**: Clean, responsive design with dark theme
- ⚡ **Fast Search**: Real-time search with fuzzy matching
- 📱 **Mobile Friendly**: Works on all devices

## Live Demo

[Visit the live site](https://arcs.fr4iser.com) (if deployed)

## Screenshots

*Add screenshots here if you have them*

## Getting Started

### Prerequisites

- Node.js 20+ and npm
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/SalvageList-Raiders.git
   cd SalvageList-Raiders
   ```

2. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173`

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker compose up --build
   ```

2. **Access the application:**
   The app will be available on port 80 (or as configured in your Traefik setup)

See [DOCKER.md](./DOCKER.md) for more detailed Docker deployment instructions.

## Usage

1. **Select a Material**: Use the search bar to find the material you need
2. **View Results**: See all items that produce that material when recycled
3. **Check Details**: Each item card shows:
   - How much of the material you get per item
   - Sell price
   - What the item recycles to
   - Rarity and category

## Contributing

We welcome contributions! Especially translations for new languages.

- **Adding Translations**: See [TRANSLATION_GUIDE.md](./TRANSLATION_GUIDE.md)
- **General Contributing**: See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Quick Translation Guide

1. Copy `frontend/src/translations/TEMPLATE.ts` to `frontend/src/translations/[language-code].ts`
2. Fill in the translations
3. Update the system files (see TRANSLATION_GUIDE.md for details)
4. Submit a Pull Request

## Tech Stack

- **Frontend**: React 19 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Deployment**: Docker + Nginx
- **Reverse Proxy**: Traefik

## Project Structure

```
SalvageList-Raiders/
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── translations/  # Translation files
│   │   └── ...
│   ├── public/
│   │   ├── icons/        # Item icons
│   │   └── items.json    # Item data
│   └── ...
├── Dockerfile            # Docker build configuration
├── docker-compose.yml    # Docker Compose configuration
├── nginx.conf            # Nginx configuration
└── ...
```

## Data Source

Item data is sourced from the [ARC Raiders Wiki](https://arc-raiders.fandom.com/wiki/Items). Icons are downloaded from the wiki and stored locally.

## License

[Add your license here]

## Acknowledgments

- ARC Raiders community for the wiki data
- All contributors who help with translations

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/SalvageList-Raiders/issues)
- **Translations**: See [TRANSLATION_GUIDE.md](./TRANSLATION_GUIDE.md)

---

Made with ❤️ for the ARC Raiders community

