# Azure Deployment Guide

This document explains how to deploy the Canada Map PoC to Azure using GitHub Actions.

## Architecture Overview

### Minimal PoC (Recommended)

```
    ┌───────────────────────────┐       ┌───────────────────────────┐
    │   POI API Container App   │       │  TileServer Container App │
    │       (ca-poi-api)        │       │     (ca-tileserver)       │
    │   *.azurecontainerapps.io │       │   *.azurecontainerapps.io │
    │         Port 5000         │       │        Port 8080          │
    └───────────────────────────┘       └───────────────────────────┘
                                                   │
                                                   │ Mounted Volume
                                                   ▼
                                    ┌───────────────────────────────┐
                                    │    Azure Blob Storage         │
                                    │   (maptiles container)        │
                                    │   - canada.mbtiles (2.6GB)    │
                                    └───────────────────────────────┘
```

Container Apps provide auto-generated HTTPS URLs (e.g., `ca-poi-api.kindgrass-abc123.canadacentral.azurecontainerapps.io`).

### With Front Door (Optional - Production)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Azure Front Door (Optional)                          │
│                     Custom domain + CDN + WAF                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
              Container Apps                      Container Apps
```

Add Front Door later if you need: custom domain, CDN caching, WAF, or global load balancing.

## Prerequisites

Infrastructure is provisioned via Terraform in a separate repository. The following resources must exist:

| Resource | Example Name | Purpose |
|----------|--------------|---------|
| Resource Group | `rg-canada-map-poc` | Container for all resources |
| Container Registry | `acrcanadamappoc` | Docker image storage |
| Storage Account | `stcanadamappoc` | Map tiles blob storage |
| Key Vault | `kv-canada-map-poc` | Secrets management |
| Container Apps Environment | `cae-canada-map-poc` | Container runtime |
| Container App (API) | `ca-poi-api` | POI API service |
| Container App (TileServer) | `ca-tileserver` | TileServer GL service |
| Front Door *(optional)* | `fd-canada-map-poc` | CDN and global routing (not needed for PoC) |

## One-Time Setup

### 1. Configure Azure Parameters (Local Development Only)

```bash
# Copy the example file (azure-params.json is gitignored)
cp azure-params.example.json azure-params.json

# Edit with your real values
code azure-params.json
```

> ⚠️ **Security**: Never commit `azure-params.json` - it's gitignored. For CI/CD, use GitHub Secrets and Variables instead (see step 3).

### 2. Upload Map Tiles to Blob Storage

The `canada.mbtiles` file is ~2.6GB and should be uploaded manually (not via CI/CD):

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "<subscription-id>"

# Upload mbtiles file
az storage blob upload \
  --account-name stcanadamappoc \
  --container-name maptiles \
  --file ./data/canada.mbtiles \
  --name canada.mbtiles \
  --auth-mode login
```

Alternatively, use Azure Storage Explorer for a GUI upload.

### 3. Configure GitHub Repository Secrets

Navigate to **Settings > Secrets and variables > Actions** in your GitHub repository.

> 🔒 **Security**: All sensitive configuration lives in GitHub Secrets/Variables, NOT in code. The `azure-params.example.json` is just a template for local reference.

#### Secrets (sensitive values - never in code)

| Secret Name | Description |
|-------------|-------------|
| `AZURE_CLIENT_ID` | Service Principal or Managed Identity client ID |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |

#### Variables (non-sensitive configuration)

| Variable Name | Example Value |
|---------------|---------------|
| `AZURE_RESOURCE_GROUP` | `rg-canada-map-poc` |
| `ACR_NAME` | `acrcanadamappoc` |
| `ACR_LOGIN_SERVER` | `acrcanadamappoc.azurecr.io` |
| `CONTAINER_APP_ENV` | `cae-canada-map-poc` |
| `API_APP_NAME` | `ca-poi-api` |
| `TILESERVER_APP_NAME` | `ca-tileserver` |

### 4. Configure OIDC Authentication

For secure, secretless authentication, configure Workload Identity Federation:

```bash
# Create federated credential for GitHub Actions
az ad app federated-credential create \
  --id <app-object-id> \
  --parameters '{
    "name": "github-actions-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:<org>/<repo>:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

## Deployment Process

### Automatic Deployment

Push to `main` branch triggers the GitHub Actions workflow:

1. **Build** - Docker images built for both services
2. **Push** - Images pushed to Azure Container Registry
3. **Deploy** - Container Apps updated with new images

### Manual Deployment

Trigger deployment manually via GitHub Actions UI:
1. Go to **Actions** tab
2. Select **Deploy to Azure Container Apps**
3. Click **Run workflow**

### Local Testing Before Deploy

```bash
# Build and test locally
docker compose up --build

# Access services
# - Map UI: http://localhost:5000
# - TileServer: http://localhost:8080
```

## File Structure

```
canada-map/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── services/
│   ├── api/
│   │   ├── app.py              # Flask API + UI
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── tileserver/
│       ├── Dockerfile          # TileServer container
│       ├── config.json         # TileServer configuration
│       └── styles/             # Map styles
├── data/
│   └── canada.mbtiles          # Map tiles (not in git)
├── docs/
│   └── AZURE-DEPLOYMENT.md     # This file
├── azure-params.example.json   # Example parameters
├── docker-compose.yml          # Local development
└── README.md
```

## Environment Configuration

### Container App Environment Variables

**POI API (`ca-poi-api`):**
| Variable | Value |
|----------|-------|
| `TILESERVER_URL` | `https://ca-tileserver.<region>.azurecontainerapps.io` |
| `PORT` | `5000` |

**TileServer (`ca-tileserver`):**
| Variable | Value |
|----------|-------|
| `MBTILES_PATH` | `/data/canada.mbtiles` |

### Storage Mount Configuration

The TileServer Container App requires a storage mount to access the mbtiles file:

```bash
# Create storage mount
az containerapp update \
  --name ca-tileserver \
  --resource-group rg-canada-map-poc \
  --set-env-vars MBTILES_PATH=/data/canada.mbtiles

# Configure volume (done in Terraform)
```

## Monitoring & Troubleshooting

### View Logs

```bash
# POI API logs
az containerapp logs show \
  --name ca-poi-api \
  --resource-group rg-canada-map-poc \
  --follow

# TileServer logs
az containerapp logs show \
  --name ca-tileserver \
  --resource-group rg-canada-map-poc \
  --follow
```

### Check Container Status

```bash
az containerapp show \
  --name ca-poi-api \
  --resource-group rg-canada-map-poc \
  --query "properties.runningStatus"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Image pull failed | Check ACR credentials and Container App identity |
| Storage mount not working | Verify blob container permissions |
| Health check failing | Check container port and startup time |
| Slow tile loading | Consider adding Front Door for CDN caching |

## Cost Comparison

### Container Apps vs App Service

| Service | Pricing | Scale to Zero | PoC Monthly Cost |
|---------|---------|---------------|------------------|
| **Container Apps (Consumption)** | Pay per vCPU-second | ✅ Yes | ~$0-5 (low traffic) |
| **App Service (Basic B1)** | ~$13/month per app | ❌ No | ~$26 (2 apps) |

**Recommendation**: Use Container Apps Consumption tier for PoC - it's essentially free when idle.

### Cost Optimization Tips

- Use **Consumption** tier for Container Apps (scales to zero)
- Enable **Cool** tier for blob storage (infrequent access)
- Set minimum replicas to 0 for auto-scale down
- **Skip Front Door** for PoC (use Container Apps built-in HTTPS URLs)
- Add Front Door later only if you need custom domain or CDN caching

## Security Considerations

- ✅ OIDC authentication (no stored secrets)
- ✅ Managed Identity for Container Apps
- ✅ Key Vault for sensitive configuration
- ✅ Private networking optional (add via Terraform)
- ✅ HTTPS enforced (Container Apps provides built-in TLS)

## Next Steps (Production)

1. Add Front Door for custom domain and CDN
2. Set up Application Insights for monitoring
3. Configure alerts for container health
4. Add staging environment slot
