# Hudu Warranty Copier

A Python script to copy warranty expiration dates from the imported configurations to the default asset layout card in Hudu. This makes warranty expiry dates easily viewable in a list format, streamlining asset management.

## Features
- Retrieves warranty expiration dates from integration cards (e.g., CW Manage) in Hudu.
- Updates the default asset layout cards with the corresponding warranty expiration dates.
- Supports paginated fetching and processing of assets.

## Requirements
- Python 3.x
- [Hudu API Key](https://support.hudu.com/hc/en-us/articles/11422780787735-REST-API)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MassoniMacaroni/Hudu-Copier.git
   cd Hudu-Copier
   ```

2. Install dependencies (if any):
   ```bash
   pip install requests
   ```

## Configuration

Update the following variables in the script `addWarrantyToCard.py` to match your environment:

- **`hudu_api_key`**: Your Hudu API key.
- **`api_url`**: Your Hudu API endpoint, e.g., `https://yourcompany.huducloud.com/api/v1/`.
- **`workstationALName`**: The name of the asset layout (e.g., "Managed Workstation").
- **`fieldNameWarrantyExpiry`**: The field name in the default asset layout where warranty expiry dates will be stored (e.g., "Warranty Expiration Date").

## Usage

Run the script:

```bash
python addWarrantyToCard.py
```

The script performs the following steps:

1. Fetches the asset layout ID for the specified asset layout.
2. Retrieves all assets using the asset layout ID, processing them in pages.
3. Extracts warranty expiration dates from integration cards.
4. Updates the default asset layout cards with the warranty expiration dates.

## Script Overview

### Functions

1. **`getAssetLayoutDetails()`**
   - Fetches the ID of the specified asset layout.
   - Returns: Asset layout ID as a string.

2. **`getAssets(assetLayoutId)`**
   - Fetches and processes all assets linked to the given asset layout ID.
   - Handles pagination and retrieves assets with warranty expiration dates.
   - Returns: A list of processed assets.

3. **`updateWarrantyExpiry(asset_id, company_id, warranty_expiration_date)`**
   - Updates the default asset layout card with the warranty expiration date.
   - Sends an HTTP PUT request to Hudu's API.

### Example Payload

The script sends payloads like the following to update warranty expiry dates:

```json
{
  "asset": {
    "custom_fields": [
      {
        "Warranty Expiration Date": "2025-12-31"
      }
    ]
  }
}
```

## Notes
- Ensure your Hudu API key has the necessary permissions to read and update assets.
- Test the script in a safe environment before running it on production data.

## Troubleshooting
- **Invalid API Key**: Verify the `hudu_api_key` and `api_url`.
- **Empty Results**: Ensure the asset layout name (`workstationALName`) is correct.
- **API Errors**: Uncomment debug lines in the `updateWarrantyExpiry` function to inspect the payload and response.

