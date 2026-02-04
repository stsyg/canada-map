# Canada Map - Self-Hosted Tile Server (Azure Maps Alternative)

A self-hosted map tile server using TileServer GL with OpenMapTiles data for Canada.
This provides a drop-in replacement for Azure Maps tile services for local/offline use cases.

> **Azure Deployment**: See [docs/AZURE-DEPLOYMENT.md](docs/AZURE-DEPLOYMENT.md) for production deployment instructions.

## Project Structure

```
canada-map/
├── .github/workflows/      # GitHub Actions CI/CD
│   └── deploy.yml          # Azure Container Apps deployment
├── services/
│   ├── api/                # Flask POI API + Map UI
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── tileserver/         # TileServer GL configuration
│       ├── Dockerfile
│       ├── config.json
│       └── styles/
├── data/                   # Map tiles (not in git)
│   └── canada.mbtiles
├── docs/                   # Documentation
│   └── AZURE-DEPLOYMENT.md
├── azure-params.example.json
├── docker-compose.yml
└── README.md
```

## Architecture

This project runs two Docker containers that work together:

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network                            │
│  ┌─────────────────────┐    ┌─────────────────────┐         │
│  │   TileServer GL     │    │   POI API (Flask)   │         │
│  │  (canada-tileserver)│    │  (canada-poi-api)   │         │
│  │   Port: 8080        │◄───│   Port: 5000        │         │
│  │   Vector/Raster     │    │   REST API + Map UI │         │
│  │   Tiles             │    │                     │         │
│  └─────────────────────┘    └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Services

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| `tileserver` | canada-tileserver | 8080 | TileServer GL - serves map tiles |
| `poi-api` | canada-poi-api | 5000 | Flask API - POI management and map UI |

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Canada map data generated (see Data Generation section)

### Start the Services

```bash
# Build and start all services
docker compose up -d --build

# View logs
docker compose logs -f
```

### Access Points

- **Map with POIs**: http://localhost:5000
- **POI REST API**: http://localhost:5000/api/pois
- **TileServer UI**: http://localhost:8080
- **Health Check**: http://localhost:5000/api/health

### Stop the Services

```bash
docker compose down
```

## API Endpoints

### TileServer GL (Port 8080)

| Endpoint | Description |
|----------|-------------|
| `/data/v3/{z}/{x}/{y}.pbf` | Vector tiles in MVT format |
| `/data/v3.json` | TileJSON metadata |
| `/styles/basic-preview/{z}/{x}/{y}.png` | Raster tiles |
| `/styles/basic-preview/style.json` | MapLibre GL style JSON |
| `/styles/basic-preview/static/{lon},{lat},{zoom}/{width}x{height}.png` | Static map image |

### POI API (Port 5000)

| Endpoint | Description |
|----------|-------------|
| `GET /` | Interactive map with POI markers |
| `GET /api/pois` | Get all POIs as JSON |
| `GET /api/pois/<country>` | Get POIs by country (canada, usa, uk, nato) |
| `GET /api/pois/region/<region>` | Get POIs by region (ontario, bc, alberta, arctic) |
| `GET /api/health` | Health check with tile server status |

### Example API Responses

```bash
# Get all POIs
curl http://localhost:5000/api/pois

# Get Canadian POIs only
curl http://localhost:5000/api/pois/canada

# Get Arctic region POIs
curl http://localhost:5000/api/pois/region/arctic

# Health check
curl http://localhost:5000/api/health
```

## Usage with MapLibre GL JS

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',
  style: 'http://localhost:8080/styles/basic-preview/style.json',
  center: [-96.0, 60.0], // Center of Canada
  zoom: 4
});
```

## Usage with Leaflet

```javascript
import L from 'leaflet';

const map = L.map('map').setView([60.0, -96.0], 4);

L.tileLayer('http://localhost:8080/styles/basic-preview/{z}/{x}/{y}.png', {
  attribution: '© OpenMapTiles © OpenStreetMap contributors'
}).addTo(map);
```

## Azure Maps → TileServer GL Migration

| Azure Maps Feature | TileServer GL Equivalent |
|-------------------|-------------------------|
| `atlas.Map` | MapLibre GL JS with custom style URL |
| Raster tiles | `/styles/basic-preview/{z}/{x}/{y}.png` |
| Vector tiles | `/data/v3/{z}/{x}/{y}.pbf` |
| Static images | `/styles/basic-preview/static/...` |
| Style JSON | `/styles/basic-preview/style.json` |

## Data Generation

To generate or update the Canada map tiles:

```bash
# Generate Canada tiles (takes ~1 hour)
docker run --rm -v "$(pwd)/data:/data" ghcr.io/onthegomap/planetiler:latest \
  --download --area=canada \
  --output=/data/canada.mbtiles \
  --maxzoom=12

# Restart services to pick up new tiles
docker compose restart tileserver
```

### Other Regions

```bash
# Ontario only (smaller, ~15 min)
docker run --rm -v "$(pwd)/data:/data" ghcr.io/onthegomap/planetiler:latest \
  --download --area=ontario \
  --output=/data/ontario.mbtiles \
  --maxzoom=12
```

## Coverage & Limitations

- **Area**: Canada (all provinces and territories)
- **Max Zoom**: 12 (configurable, increase for more detail)
- **Bounds**: -141.0° to -52.0° longitude, 41.0° to 84.0° latitude

## Development

### Running Flask App Locally (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TILESERVER_URL=http://localhost:8080
export TILESERVER_PUBLIC_URL=http://localhost:8080

# Run the app
python app.py
```

### Building Docker Images

```bash
# Build POI API image only
docker compose build poi-api

# Rebuild from scratch
docker compose build --no-cache
```

## Troubleshooting

**Containers won't start:**
```bash
docker compose logs
```

**Tiles not rendering:**
- Check that `canada.mbtiles` exists in the `data/` folder
- Verify TileServer is healthy: `curl http://localhost:8080/health`

**POI API can't connect to TileServer:**
- Check both containers are on the same network: `docker network ls`
- Verify TileServer is running: `docker compose ps`

## Attribution

- Tiles: © OpenMapTiles
- Data: © OpenStreetMap contributors
- Tile Generation: Planetiler
