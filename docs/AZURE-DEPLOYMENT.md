# Azure Deployment Guide

This document explains the Azure deployment architecture for the Canada Map PoC.

> **Infrastructure Setup**: For step-by-step infrastructure provisioning, see [AZURE-INFRASTRUCTURE.md](AZURE-INFRASTRUCTURE.md).

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Azure Container Apps Environment                         │
│                        (cae-canada-map-lab)                                 │
│                                                                             │
│   ┌─────────────────────────┐       ┌─────────────────────────────────┐    │
│   │     ca-poi-api          │       │       ca-tileserver             │    │
│   │   *.azurecontainerapps  │──────▶│     *.azurecontainerapps        │    │
│   │     Port 5000           │       │       Port 8080                 │    │
│   │   0.5 CPU / 1Gi         │       │     2 CPU / 4Gi                 │    │
│   │                         │       │   (2.7GB image with mbtiles)    │    │
│   └─────────────────────────┘       └─────────────────────────────────┘    │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
                    │
                    │ Pull images (Managed Identity - passwordless)
                    ▼
        ┌─────────────────────┐
        │   Azure Container   │
        │   Registry (Basic)  │
        │   acr<random>       │
        └─────────────────────┘
```

### Services

| Service | Purpose | Resources | Image Size |
|---------|---------|-----------|------------|
| **ca-poi-api** | Flask app with Map UI and REST API | 0.5 CPU / 1Gi | ~150MB |
| **ca-tileserver** | TileServer GL with baked-in mbtiles | 2 CPU / 4Gi | ~2.7GB |

### Key URLs

After deployment, your services will be available at:

- **POI API**: `https://ca-poi-api.<random>.<region>.azurecontainerapps.io`
- **TileServer**: `https://ca-tileserver.<random>.<region>.azurecontainerapps.io`

## Design Decisions

### Why Bake mbtiles into Docker Image?

We bake the 2.6GB `canada.mbtiles` file directly into the TileServer Docker image instead of using Azure Files mount because:

1. **Azure Policy Constraints**: Many enterprise Azure subscriptions have policies that disable storage key-based authentication. Azure Files mount for Container Apps requires storage keys.
2. **Simplicity**: No additional storage configuration needed
3. **Portability**: Image is self-contained and can run anywhere

Trade-off: Image is 2.7GB and takes ~5 minutes to push to ACR.

### Why Managed Identity?

Container Apps use Managed Identity to pull images from ACR:
- No passwords or secrets to manage
- Automatic credential rotation
- No Key Vault needed for this use case

### Why Consumption Tier?

- **Scales to zero** when idle (cost: $0)
- Perfect for PoC/demo workloads
- Automatically scales up when requests come in

## GitHub Actions CI/CD

The workflow file at `.github/workflows/deploy.yml` supports **manual deployment only**.

> **Note**: Automatic deployment on push to `main` is disabled. The workflow is configured for manual trigger via `workflow_dispatch`. To enable automatic deployment, uncomment the `push` trigger in the workflow file.

### Manual Deployment

1. Go to **Actions** tab in GitHub
2. Select **Deploy to Azure Container Apps**
3. Click **Run workflow**
4. Choose which services to deploy

### Required GitHub Secrets

Configure these in **Settings > Secrets and variables > Actions**:

| Secret | Description |
|--------|-------------|
| `AZURE_CLIENT_ID` | Service Principal client ID |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |

### Required GitHub Variables

| Variable | Example Value |
|----------|---------------|
| `AZURE_RESOURCE_GROUP` | `rg-canada-map-lab` |
| `ACR_NAME` | `acrf85f730f` |
| `ACR_LOGIN_SERVER` | `acrf85f730f.azurecr.io` |
| `CONTAINER_APP_ENV` | `cae-canada-map-lab` |
| `API_APP_NAME` | `ca-poi-api` |
| `TILESERVER_APP_NAME` | `ca-tileserver` |

## Environment Variables

### POI API Container

| Variable | Value | Purpose |
|----------|-------|---------|
| `TILESERVER_URL` | `https://ca-tileserver.<domain>` | Internal tile requests |
| `TILESERVER_PUBLIC_URL` | `https://ca-tileserver.<domain>` | Browser tile requests |

### TileServer Container

| Variable | Value | Purpose |
|----------|-------|---------|
| `PUBLIC_URL` | `https://ca-tileserver.<domain>` | Correct URL generation for tiles/fonts |

## TileServer Configuration

The TileServer requires specific configuration to work behind a reverse proxy:

### config.json

```json
{
    "options": {
        "paths": {
            "root": "/data",
            "styles": "styles",
            "fonts": "/usr/src/app/node_modules/tileserver-gl-styles/fonts",
            "mbtiles": ""
        },
        "serveAllStyles": true,
        "serveStaticMaps": false
    },
    "styles": {
        "basic": { "style": "basic/style.json" },
        "osm-bright": { "style": "osm-bright/style.json" }
    },
    "data": {
        "canada": { "mbtiles": "canada.mbtiles" }
    }
}
```

**Important**: The `fonts` path must point to the built-in TileServer fonts location, not `/data/fonts`.

### PUBLIC_URL Environment Variable

TileServer must know its public URL to generate correct tile/font URLs. This is passed via `PUBLIC_URL` environment variable and handled in `Dockerfile.azure`:

```dockerfile
ENV PUBLIC_URL=""
CMD ["sh", "-c", "if [ -n \"$PUBLIC_URL\" ]; then exec node /usr/src/app/ --public_url \"$PUBLIC_URL\"; else exec node /usr/src/app/; fi"]
```

## Local Development

```bash
# Start services locally
docker compose up -d --build

# Access points
# - Map UI: http://localhost:5000
# - TileServer: http://localhost:8080
```

## Monitoring

### View Logs

```bash
# POI API logs
az containerapp logs show \
  --name ca-poi-api \
  --resource-group rg-canada-map-lab \
  --tail 50

# TileServer logs
az containerapp logs show \
  --name ca-tileserver \
  --resource-group rg-canada-map-lab \
  --tail 50
```

### Health Checks

```bash
# TileServer health
curl https://ca-tileserver.<domain>/health

# POI API health
curl https://ca-poi-api.<domain>/api/health
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Map loads but no labels** | Fonts not accessible | Check `fonts` path in config.json points to `/usr/src/app/node_modules/tileserver-gl-styles/fonts` |
| **Malformed tile URLs** | Missing PUBLIC_URL | Set `PUBLIC_URL` env var on TileServer Container App |
| **Blank map on POI API** | Wrong style path | Use `osm-bright` style, not `basic-preview` |
| **Container won't start** | Not enough resources | TileServer needs 2 CPU / 4Gi for 2.6GB mbtiles |
| **Image pull failed** | ACR auth | Ensure `--registry-identity system` is set |

## Cost Estimate

| Resource | SKU | Monthly Cost |
|----------|-----|--------------|
| Container Registry | Basic | ~$5 |
| Container Apps (idle) | Consumption | $0 |
| Container Apps (active) | Consumption | ~$20 |
| **Total (idle)** | | **~$5** |
| **Total (active)** | | **~$25** |

## Security Notes

- ✅ HTTPS enforced (Container Apps provides built-in TLS)
- ✅ Managed Identity for ACR (no secrets)
- ✅ No storage keys or connection strings
- ✅ Scales to zero when idle

## Future Improvements

- Add Azure Front Door for custom domain and CDN caching
- Enable Application Insights for monitoring
- Configure auto-scaling rules based on CPU/memory
- Add staging environment for testing
