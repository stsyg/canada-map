# Azure Infrastructure Setup Guide

This document provides step-by-step instructions to provision Azure infrastructure for the Canada Map PoC.

## Prerequisites

- Azure CLI installed and configured (`az login`)
- Docker installed locally
- Access to an Azure subscription

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        Azure Container Apps                                 │
│                                                                             │
│   ┌─────────────────────────┐       ┌─────────────────────────────────┐    │
│   │     ca-poi-api          │       │       ca-tileserver             │    │
│   │     (Flask + UI)        │──────▶│       (TileServer GL)           │    │
│   │     Port 5000           │       │       Port 8080                 │    │
│   │     0.5 CPU / 1Gi       │       │       2 CPU / 4Gi               │    │
│   └─────────────────────────┘       │  (mbtiles baked into image)     │    │
│                                     └─────────────────────────────────┘    │
│                                                                             │
│   Container Apps Environment: cae-canada-map-lab                            │
└────────────────────────────────────────────────────────────────────────────┘
                    │
                    │ Pull images (Managed Identity)
                    ▼
        ┌─────────────────────┐
        │   Azure Container   │
        │   Registry (Basic)  │
        │   acr<random>       │
        └─────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Bake mbtiles into Docker image** | Azure Files mount requires storage key auth, which may be blocked by Azure Policy. Baking the 2.6GB mbtiles into the image avoids this issue. |
| **Managed Identity for ACR** | Passwordless authentication - no secrets to manage |
| **Consumption tier** | Scales to zero when idle, cost-effective for PoC |
| **2 CPU / 4Gi for TileServer** | Required for loading 2.6GB mbtiles file at startup |
| **No Key Vault** | Not needed for this PoC - using managed identity instead |

## Step 1: Generate Unique Resource Names

Azure resource names must be globally unique. Use this command to generate a random suffix:

```bash
# Generate random suffix (8 hex characters)
RANDOM_SUFFIX=$(printf '%04x%04x' $RANDOM $RANDOM)
echo "Random suffix: $RANDOM_SUFFIX"

# Example output: f85f730f
```

Use this suffix for all resources:

| Resource | Naming Pattern | Example |
|----------|---------------|---------|
| Resource Group | `rg-canada-map-<env>` | `rg-canada-map-lab` |
| Container Registry | `acr<suffix>` | `acrf85f730f` |
| Container Apps Env | `cae-canada-map-<env>` | `cae-canada-map-lab` |
| POI API App | `ca-poi-api` | `ca-poi-api` |
| TileServer App | `ca-tileserver` | `ca-tileserver` |

## Step 2: Set Environment Variables

```bash
# Your Azure subscription
export SUBSCRIPTION_ID="your-subscription-id"
export LOCATION="canadacentral"
export ENV_NAME="lab"
export RANDOM_SUFFIX=$(printf '%04x%04x' $RANDOM $RANDOM)

# Resource names
export RESOURCE_GROUP="rg-canada-map-${ENV_NAME}"
export ACR_NAME="acr${RANDOM_SUFFIX}"
export CAE_NAME="cae-canada-map-${ENV_NAME}"
export POI_API_APP="ca-poi-api"
export TILESERVER_APP="ca-tileserver"

echo "ACR Name: $ACR_NAME"
```

## Step 3: Create Resource Group

```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

## Step 4: Create Azure Container Registry

```bash
# Create ACR (Basic SKU is sufficient for PoC)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled false

# Get ACR login server
export ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
echo "ACR Login Server: $ACR_LOGIN_SERVER"
```

## Step 5: Create Container Apps Environment

```bash
az containerapp env create \
  --name $CAE_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

## Step 6: Build and Push Docker Images

### 6.1 Login to ACR

```bash
az acr login --name $ACR_NAME
```

### 6.2 Build and Push POI API Image

```bash
docker build -t ${ACR_LOGIN_SERVER}/poi-api:v1 ./services/api
docker push ${ACR_LOGIN_SERVER}/poi-api:v1
```

### 6.3 Build TileServer Image with Baked mbtiles

The TileServer image includes the 2.6GB canada.mbtiles file. This requires a multi-stage build:

```bash
# First, create a scratch image with just the mbtiles file
docker build -t mbtiles:latest - <<EOF
FROM scratch
COPY data/canada.mbtiles /canada.mbtiles
EOF

# Build the TileServer image with baked mbtiles
docker build -f services/tileserver/Dockerfile.azure \
  -t ${ACR_LOGIN_SERVER}/tileserver:v1 \
  ./services/tileserver

# Push to ACR (this will take a while due to 2.7GB image size)
docker push ${ACR_LOGIN_SERVER}/tileserver:v1
```

## Step 7: Create POI API Container App

```bash
az containerapp create \
  --name $POI_API_APP \
  --resource-group $RESOURCE_GROUP \
  --environment $CAE_NAME \
  --image ${ACR_LOGIN_SERVER}/poi-api:v1 \
  --target-port 5000 \
  --ingress external \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-identity system \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 0 \
  --max-replicas 1

# Get the FQDN
export POI_API_FQDN=$(az containerapp show --name $POI_API_APP --resource-group $RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv)
echo "POI API URL: https://$POI_API_FQDN"
```

## Step 8: Create TileServer Container App

```bash
# Get the TileServer URL (we'll need it for the POI API)
export TILESERVER_URL="https://ca-tileserver.$(az containerapp env show --name $CAE_NAME --resource-group $RESOURCE_GROUP --query 'properties.defaultDomain' -o tsv)"

az containerapp create \
  --name $TILESERVER_APP \
  --resource-group $RESOURCE_GROUP \
  --environment $CAE_NAME \
  --image ${ACR_LOGIN_SERVER}/tileserver:v1 \
  --target-port 8080 \
  --ingress external \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-identity system \
  --cpu 2 \
  --memory 4Gi \
  --min-replicas 0 \
  --max-replicas 1 \
  --env-vars "PUBLIC_URL=${TILESERVER_URL}"

# Get the FQDN
export TILESERVER_FQDN=$(az containerapp show --name $TILESERVER_APP --resource-group $RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv)
echo "TileServer URL: https://$TILESERVER_FQDN"
```

## Step 9: Configure POI API Environment Variables

Update the POI API to point to the TileServer:

```bash
az containerapp update \
  --name $POI_API_APP \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars \
    "TILESERVER_URL=https://${TILESERVER_FQDN}" \
    "TILESERVER_PUBLIC_URL=https://${TILESERVER_FQDN}"
```

## Step 10: Verify Deployment

```bash
# Check TileServer health
curl -s https://${TILESERVER_FQDN}/health
# Expected: OK

# Check fonts are accessible
curl -sI "https://${TILESERVER_FQDN}/fonts/Noto%20Sans%20Regular/0-255.pbf" | head -1
# Expected: HTTP/2 200

# Check tile data
curl -s "https://${TILESERVER_FQDN}/data/canada.json" | jq '.tiles[0]'
# Expected: URL with correct format

# Check POI API
curl -s "https://${POI_API_FQDN}/api/pois" | jq 'length'
# Expected: 63 (or number of POIs)

# Open in browser
echo "Map URL: https://${POI_API_FQDN}"
```

## Updating Images

When you need to deploy new versions:

```bash
# Build new version
docker build -t ${ACR_LOGIN_SERVER}/poi-api:v2 ./services/api
docker push ${ACR_LOGIN_SERVER}/poi-api:v2

# Update Container App
az containerapp update \
  --name $POI_API_APP \
  --resource-group $RESOURCE_GROUP \
  --image ${ACR_LOGIN_SERVER}/poi-api:v2
```

## Troubleshooting

### View Container Logs

```bash
az containerapp logs show \
  --name $TILESERVER_APP \
  --resource-group $RESOURCE_GROUP \
  --tail 50
```

### Check Revision Status

```bash
az containerapp revision list \
  --name $TILESERVER_APP \
  --resource-group $RESOURCE_GROUP \
  -o table
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Container won't start** | Image too large, timeout | Increase CPU/memory, check startup probe settings |
| **Fonts return 400** | Fonts path not configured | Set `fonts` path in config.json to `/usr/src/app/node_modules/tileserver-gl-styles/fonts` |
| **Malformed tile URLs** | Missing PUBLIC_URL | Set `PUBLIC_URL` environment variable on TileServer |
| **Map loads but no labels** | Fonts not accessible | Check fonts endpoint returns 200 |
| **Image pull failed** | ACR auth issue | Verify managed identity is configured: `--registry-identity system` |

## Cleanup

To delete all resources:

```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Cost Estimate

| Resource | SKU | Monthly Cost (Idle) | Monthly Cost (Active) |
|----------|-----|---------------------|----------------------|
| Container Registry | Basic | ~$5 | ~$5 |
| Container Apps (POI API) | Consumption | $0 (scales to 0) | ~$5 |
| Container Apps (TileServer) | Consumption | $0 (scales to 0) | ~$15 |
| **Total** | | **~$5** | **~$25** |

> **Note**: Container Apps Consumption tier scales to zero when idle, making it very cost-effective for PoC/demo workloads.
