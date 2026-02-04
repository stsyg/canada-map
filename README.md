# Canada Map PoC - Self-Hosted Tile Server

A self-hosted map tile server using TileServer GL with OpenMapTiles data for Canada.
Provides a cost-effective alternative to Azure Maps for internal/PoC use cases.

## Live Demo (Azure)

- **Map with POIs**: https://ca-poi-api.whitedune-f8591151.canadacentral.azurecontainerapps.io
- **TileServer**: https://ca-tileserver.whitedune-f8591151.canadacentral.azurecontainerapps.io

## Features

- 🗺️ **Full Canada map** with provinces, cities, roads, water features
- 📍 **63 Military Installations** - Canada, USA, UK & NATO bases
- 🔍 **Filter markers** by country and branch (Army, Navy, Air Force, Special Forces)
- 🎨 **OSM Bright style** - clean, detailed map rendering
- 🐳 **Docker-based** - easy local development
- ☁️ **Azure Container Apps** - serverless deployment

## Project Structure

```
canada-map/
├── .github/workflows/      # GitHub Actions (manual deploy)
│   └── deploy.yml
├── services/
│   ├── api/                # Flask POI API + Map UI
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── tileserver/         # TileServer GL
│       ├── Dockerfile              # Local development
│       ├── Dockerfile.azure        # Azure (baked mbtiles)
│       ├── config.json
│       └── styles/
├── data/                   # Map tiles (not in git)
│   └── canada.mbtiles      # 2.6GB - generate locally
├── docs/
│   ├── AZURE-DEPLOYMENT.md     # Deployment guide
│   └── AZURE-INFRASTRUCTURE.md # Infrastructure setup
├── docker-compose.yml
└── README.md
```

## Quick Start (Local)

### Prerequisites

- Docker and Docker Compose
- ~3GB disk space for map tiles

### 1. Generate Map Tiles

```bash
# Generate Canada tiles (~1 hour, 2.6GB output)
docker run --rm -v "$(pwd)/data:/data" ghcr.io/onthegomap/planetiler:latest \
  --download --area=canada \
  --output=/data/canada.mbtiles \
  --maxzoom=12
```

### 2. Start Services

```bash
docker compose up -d --build
```

### 3. Access the Map

- **Map with POIs**: http://localhost:5000
- **TileServer UI**: http://localhost:8080
- **POI API**: http://localhost:5000/api/pois

### 4. Stop Services

```bash
docker compose down
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network                            │
│  ┌─────────────────────┐    ┌─────────────────────┐         │
│  │   TileServer GL     │    │   POI API (Flask)   │         │
│  │  (canada-tileserver)│    │  (canada-poi-api)   │         │
│  │   Port: 8080        │◄───│   Port: 5000        │         │
│  │   Vector Tiles      │    │   REST API + Map UI │         │
│  └─────────────────────┘    └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

### POI API (Port 5000)

| Endpoint | Description |
|----------|-------------|
| `GET /` | Interactive map with POI markers |
| `GET /api/pois` | All POIs as JSON |
| `GET /api/pois?country=canada` | Filter by country |
| `GET /api/pois?category=navy` | Filter by branch |
| `GET /api/health` | Health check |

### TileServer (Port 8080)

| Endpoint | Description |
|----------|-------------|
| `/styles/osm-bright/style.json` | MapLibre GL style |
| `/data/canada/{z}/{x}/{y}.pbf` | Vector tiles |
| `/fonts/{fontstack}/{range}.pbf` | Font glyphs |
| `/health` | Health check |

## Usage with MapLibre GL JS

```javascript
const map = new maplibregl.Map({
  container: 'map',
  style: 'http://localhost:8080/styles/osm-bright/style.json',
  center: [-96.0, 56.0],
  zoom: 3.5
});
```

## Azure Deployment

See the docs folder for Azure deployment:

- [AZURE-INFRASTRUCTURE.md](docs/AZURE-INFRASTRUCTURE.md) - Step-by-step infrastructure setup
- [AZURE-DEPLOYMENT.md](docs/AZURE-DEPLOYMENT.md) - Architecture and configuration

### Key Points

- **Container Apps** (Consumption tier) - scales to zero
- **Managed Identity** for ACR - no secrets
- **mbtiles baked into image** - no Azure Files mount needed
- **Cost**: ~$5/month idle, ~$25/month active

## Development

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TILESERVER_URL` | `http://localhost:8080` | TileServer URL for internal requests |
| `TILESERVER_PUBLIC_URL` | `http://localhost:8080` | TileServer URL for browser |

### Regenerate Tiles

```bash
# Canada (full) - ~1 hour
docker run --rm -v "$(pwd)/data:/data" ghcr.io/onthegomap/planetiler:latest \
  --download --area=canada \
  --output=/data/canada.mbtiles \
  --maxzoom=12

# Ontario only - ~15 min
docker run --rm -v "$(pwd)/data:/data" ghcr.io/onthegomap/planetiler:latest \
  --download --area=ontario \
  --output=/data/ontario.mbtiles \
  --maxzoom=12
```

### Build for Azure

```bash
# Create scratch image with mbtiles
docker build -t mbtiles:latest - <<EOF
FROM scratch
COPY data/canada.mbtiles /canada.mbtiles
EOF

# Build TileServer with baked mbtiles
docker build -f services/tileserver/Dockerfile.azure \
  -t tileserver:azure \
  ./services/tileserver
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Tiles not loading** | Check `canada.mbtiles` exists in `data/` folder |
| **No city labels** | Zoom in (labels appear at zoom 3+) |
| **Container won't start** | Run `docker compose logs` to see errors |
| **Health check failing** | Verify TileServer is running: `curl localhost:8080/health` |

## Coverage

- **Area**: Canada (all provinces and territories)
- **Zoom levels**: 0-12
- **Bounds**: -141.0° to -52.0° W, 41.0° to 84.0° N

## Attribution

- Map tiles: © [OpenMapTiles](https://openmaptiles.org/)
- Map data: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
- Tile generation: [Planetiler](https://github.com/onthegomap/planetiler)
- Tile server: [TileServer GL](https://github.com/maptiler/tileserver-gl)

## License

MIT
